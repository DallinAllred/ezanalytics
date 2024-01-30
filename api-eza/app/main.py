from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from .dependencies import get_query_token, get_token_header
# from .internal import admin
from .routers import user_routes
from .routers import chart_routes

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()

origins = [
    'http://localhost',
    'http://vue:5050',
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(user_routes.router)
app.include_router(chart_routes.router)
# app.include_router(items.router)
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}