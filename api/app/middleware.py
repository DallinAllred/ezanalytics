import os
from datetime import datetime, timedelta
from fastapi import Request
from fastapi.responses import JSONResponse
from .models.db import redis_client

ERROR_HEADERS = {
    'Access-Control-Allow-Origin': os.getenv('ORIGINS').split(',')[0],
    'Access-Control-Allow-Credentials': 'true'
    }

async def validate_session(request: Request, call_next):
    path = request.url.path
    if path == '/api/auth/logout'\
        or path == '/api/auth/login'\
            or request.method == 'OPTIONS':
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
                            headers=ERROR_HEADERS)
    now = datetime.now()
    timeout = redis_client.hget(session_id, 'timeout')
    timeout = datetime.strptime(timeout, '%d/%m/%Y, %H:%M:%S')
    if now > timeout:
        print('Session timed out')
        return JSONResponse(status_code=401,
                            content={'error': 'Expired credentials'},
                            headers=ERROR_HEADERS)
    timeout = datetime.now() + timedelta(minutes=30)
    timeout = timeout.strftime('%d/%m/%Y, %H:%M:%S')
    redis_client.hset(session_id, 'timeout', timeout)
    return await call_next(request)

async def validate_permissions(request: Request, call_next):
    path = request.url.path
    if path == '/api/auth/logout'\
        or path == '/api/auth/login'\
            or request.method == 'OPTIONS':
        return await call_next(request)
    try:
        session_id = request.cookies['session_id']
    except KeyError:
        return JSONResponse(status_code=401,
                            content={'error': 'Invalid credentials'},
                            headers=ERROR_HEADERS)
    user = redis_client.hgetall(session_id)
    if user == {}:
        return JSONResponse(status_code=401,
                            content={'error': 'Unknown user'},
                            headers=ERROR_HEADERS)
    user = {key: bool(int(val)) if val == '0' or val == '1'
            else val for key, val in user.items()}

    if user['admin'] or '/api/profile' in path:
        return await call_next(request)
    if '/api/connections' in path and user['connections']:
        return await call_next(request)
    if request.method == 'GET':
        if ('/api/chart' in path or '/api/dash' in path or '/api/sources' in path) \
            and user['viewer']:
            return await call_next(request)
    if request.method == 'POST' or \
        request.method == 'PUT' or \
        request.method == 'DELETE':
        if '/api/chart' in path and user['chart_builder']:
            return await call_next(request)
        if '/api/dash' in path and user['dash_builder']:
            return await call_next(request)
    return JSONResponse(status_code=403,
                        content={'error': 'Unauthorized'},
                        headers=ERROR_HEADERS)
