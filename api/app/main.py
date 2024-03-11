from datetime import datetime, timedelta
from fastapi import Cookie, Depends, FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from typing import Annotated

# from .dependencies import get_query_token, get_token_header
# from .internal import admin
from .auth import auth
from .routers import user_routes
from .routers import chart_routes
from .routers import dashboard_routes
from .routers import source_routes

from .models.db import redis_client

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()

origins = [
    'http://localhost:8080',
    'http://vue:5050',
    'http://lvh.me', 'http://lvh.me:8080'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=origins
)

@app.middleware('http')
async def validate_session(call_next, request: Request, response: Response,
                           session_id: Annotated[str | None, Cookie()] = None,):
    if not session_id:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return

    now = datetime.now()
    expiration = redis_client.hget(session_id, 'expiration')
    expiration = datetime.strptime(expiration, '%d/%m/%Y, %H:%M:%S')
    if now > expiration:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return
    expiration = datetime.now() + timedelta(minutes=30)
    expiration = expiration.strftime('%d/%m/%Y, %H:%M:%S')
    redis_client.hset(session_id, 'expiration', expiration)
    call_next(request)

app.include_router(auth.router)
app.include_router(user_routes.router)
app.include_router(chart_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(source_routes.router)

@app.get("/")
async def root():
    return {"message": "Welcome to EZAnalytics!"}