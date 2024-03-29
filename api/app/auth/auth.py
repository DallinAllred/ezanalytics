from argon2 import PasswordHasher
from datetime import datetime, timedelta
from fastapi import APIRouter, Cookie, Response, status
from pydantic import BaseModel
from typing import Annotated

from ..models.db import eza_pool, redis_client
from ..models.user_model import User

router = APIRouter(
    prefix='/api/auth',
    responses={404: {'description': 'Not found'}}
)

class Credentials(BaseModel):
    '''
    Extended Pydantic BaseModel to handle a login request
    Fields:
        username: str
        password: str
    '''
    username: str
    password: str


class Auth:
    @staticmethod
    def generate_password(password):
        'Creates a hash from the supplied password'
        ph = PasswordHasher()
        hash = ph.hash(password)
        return hash

    @staticmethod
    def login(username, password):
        '''
        Verifies that the password hashes to match the password associated with the username
        '''
        query = 'SELECT user_id, username, password FROM users WHERE username=%s;'
        with eza_pool.connection() as conn:
            result = conn.execute(query, [username])
            data = result.fetchall()
        if len(data) != 1:
            raise ValueError
        user_id = data[0][0]
        hash = data[0][2]
        ph = PasswordHasher()
        ph.verify(hash, password)
        session_id = ph.hash(f'{username}{datetime.now()}')
        return session_id, user_id
    
    @staticmethod
    def update_password(user_id, hash):
        '''
        Update the user's password hash
        Expects that the supplied hash is an argon2 hash (not plaintext)
        '''
        query = 'UPDATE users SET password=%s WHERE user_id=%s'
        with eza_pool.connection() as conn:
            result = conn.execute(query, [hash, user_id])
            conn.commit()
    
    @staticmethod
    def validate_password(user_id, password):
        'Verify that the supplied password matches the hash in the database'
        query = 'SELECT password from users WHERE user_id=%s'
        with eza_pool.connection() as conn:
            result = conn.execute(query, [user_id])
            data = result.fetchall()
        if len(data) != 1:
            raise ValueError
        hash = data[0][0]
        ph = PasswordHasher()
        ph.verify(hash, password)
        return True

    @staticmethod
    def create_session(session_id, user_info, timeout):
        'Create a session in Redis'
        map = {
                'username': user_info['username'],
                'user_id': int(user_info['user_id']),
                'admin': int(user_info['admin']),
                'viewer': int(user_info['viewer']),
                'chart_builder': int(user_info['chart_builder']),
                'dash_builder': int(user_info['dash_builder']),
                'connections': int(user_info['connections']),
                'timeout': timeout
            }
        redis_client.hset(session_id, mapping=map)
        return map

    @staticmethod
    def clean_sessions():
        'Remove expired sessions'
        now = datetime.now()
        for session in redis_client.keys():
            timeout = redis_client.hget(session, 'timeout')
            timeout = datetime.strptime(timeout, '%d/%m/%Y, %H:%M:%S')
            if timeout < now:
                redis_client.delete(session)

    @staticmethod
    def delete_session(session_id):
        'Delete the indicated session'
        redis_client.delete(session_id)

    @staticmethod
    def get_permissions(session_id):
        'Retrieve session permissions'
        info = redis_client.hgetall(session_id)
        del info['username']
        del info['timeout']
        return info

@router.put('/login', status_code=200)
async def login_user(credentials: Credentials, response: Response):
    'Handle a login request'
    try:
        # Check password and username match
        session_id, user_id = Auth.login(credentials.username, credentials.password)
        # Get user permissions and transform data
        user_info = User.get_user(user_id)
        user_info = user_info[0]
        user_info = {key: 1 if val == True else 0 if val == None else val for key, val in user_info.items()}
        session_id = session_id.split(',')[-1][4:]
        timeout = datetime.now() + timedelta(minutes=30)
        timeout = timeout.strftime('%d/%m/%Y, %H:%M:%S')
        # Create Redis session
        session_map = Auth.create_session(session_id, user_info, timeout)
        response.set_cookie(
            key='session_id',
            value=session_id,
            max_age=36_000
        )
        Auth.clean_sessions()
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return
    del session_map['timeout']
    return session_map

@router.put('/logout', status_code=200)
async def logout_user(response: Response,
                      session_id: Annotated[str | None, Cookie()] = None):
    'Close the session'
    if session_id:
        Auth.delete_session(session_id)
        response.set_cookie(
            key='session_id',
            value=session_id,
            max_age=0
        )
    return True

@router.get('/permissions')
async def get_permission(response: Response,
                         session_id: Annotated[str | None, Cookie()] = None):
    'Handle request for user permissions'
    if not session_id:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return
    permissions = Auth.get_permissions(session_id)
    permissions = {key: bool(val) for key, val in enumerate(permissions)}
    return permissions
