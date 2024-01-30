from fastapi import APIRouter
from ..models import user_model

router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_users():
    data = user_model.User.get_users()
    return data

@router.get("/{user_id}")
async def read_user(user_id):
    data = user_model.User.get_user(user_id)
    return data

@router.post("/")
async def create_user():
    return [{"action": "Adding user"}]

@router.put("/{user_id}")
async def update_user(user_id):
    return [{"action": f'Updating user {user_id}'}]

@router.delete("/{user_id}")
async def delete_user(user_id):
    return [{"user_id": user_id, "action": "Delete"}]