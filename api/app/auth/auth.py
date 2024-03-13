from argon2 import PasswordHasher

from datetime import datetime, timedelta

from fastapi import APIRouter, Cookie, Response, status
from pydantic import AliasGenerator, BaseModel
from typing import Annotated, Any

from ..models.db import eza_pool, redis_client
from ..models.user_model import User

router = APIRouter(
    prefix='/api/auth',
    responses={404: {'description': 'Not found'}}
)

class Credentials(BaseModel):
    username: Any
    password: Any


class Auth:    
    @staticmethod
    def login(username, password):
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
    def create_session(session_id, user_info, timeout):
        redis_client.hset(
            session_id,
            mapping={
                'username': user_info['username'],
                'admin': int(user_info['admin']),
                'viewer': int(user_info['viewer']),
                'chart_builder': int(user_info['chart_builder']),
                'dash_builder': int(user_info['dash_builder']),
                'connections': int(user_info['connections']),
                'timeout': timeout
            }
        )

    @staticmethod
    async def clean_sessions():
        now = datetime.now()
        for session in redis_client.keys():
            timeout = redis_client.hget(session, 'timeout')
            datetime.strptime(timeout, '%d/%m/%Y, %H:%M:%S')
            if timeout < now:
                redis_client.delete(session)

    @staticmethod
    def delete_session(session_id):
        redis_client.delete(session_id)

    @staticmethod
    def get_permissions(session_id):
        info = redis_client.hgetall(session_id)
        del info['username']
        del info['timeout']
        return info


@router.put('/login', status_code=200)
async def login_user(credentials: Credentials, response: Response):
    try:
        session_id, user_id = Auth.login(credentials.username, credentials.password)
        user_info = User.get_user(user_id)
        user_info = user_info[0]
        session_id = session_id.split(',')[-1][4:]
        timeout = datetime.now() + timedelta(minutes=30)
        timeout = timeout.strftime('%d/%m/%Y, %H:%M:%S')
        Auth.create_session(session_id, user_info, timeout)
        response.set_cookie(
            key='session_id',
            value=session_id,
            max_age=36_000
        )
        Auth.clean_sessions()
    except Exception as e:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return
    return

@router.put('/logout', status_code=200)
async def logout_user(response: Response,
                      session_id: Annotated[str | None, Cookie()] = None):
    print('Logging out')
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
    if not session_id:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return
    permissions = Auth.get_permissions(session_id)
    permissions = {key: bool(val) for key, val in enumerate(permissions)}
    return permissions
