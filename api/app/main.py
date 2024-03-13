from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from .auth import auth
from .middleware import validate_session, validate_permissions
from .routers import user_routes
from .routers import chart_routes
from .routers import dashboard_routes
from .routers import source_routes

app = FastAPI()

origins = [
    'http://localhost:8080',
    'http://localhost',
    'http://vue:5050',
    'http://lvh.me', 'http://lvh.me:8080', 'http://lvh.me:5050'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.add_middleware(BaseHTTPMiddleware, dispatch=validate_session)
app.add_middleware(BaseHTTPMiddleware, dispatch=validate_permissions)

app.include_router(auth.router)
app.include_router(user_routes.router)
app.include_router(chart_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(source_routes.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the EZAnalytics API!"}