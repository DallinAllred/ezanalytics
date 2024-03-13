from datetime import datetime, timedelta
from fastapi import Request
from fastapi.responses import JSONResponse
from .models.db import redis_client

async def validate_session(request: Request, call_next):
    path = request.url.path
    if path == '/api/auth/logout' or path == '/api/auth/login':
        response = await call_next(request)
        return response
    try:
        session_id = request.cookies['session_id']
        session = redis_client.hkeys(session_id)
        if len(session) == 0:
            raise KeyError
    except KeyError as e:
        print('No session found')
        return JSONResponse(status_code=401,
                            content={'error': 'Invalid credentials'},
                            headers={
                                'Access-Control-Allow-Origin': 'http://lvh.me:8080',
                                'Access-Control-Allow-Credentials': 'true'
                                })
    now = datetime.now()
    timeout = redis_client.hget(session_id, 'timeout')
    timeout = datetime.strptime(timeout, '%d/%m/%Y, %H:%M:%S')
    if now > timeout:
        print('Session timed out')
        return JSONResponse(status_code=401,
                            content={'error': 'Expired credentials'},
                            headers={
                                'Access-Control-Allow-Origin': 'http://lvh.me:8080',
                                'Access-Control-Allow-Credentials': 'true'
                                })
    timeout = datetime.now() + timedelta(minutes=30)
    timeout = timeout.strftime('%d/%m/%Y, %H:%M:%S')
    redis_client.hset(session_id, 'timeout', timeout)
    return await call_next(request)