from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/{user_id}")
async def read_users(user_id):
    return [{"user_id": user_id}]

@router.post("/")
async def create_user():
    return [{"action": "Adding user"}]

@router.put("/{user_id}")
async def update_user(user_id):
    return [{"action": f'Updating user {user_id}'}]

@router.delete("/{user_id}")
async def delete_user(user_id):
    return [{"user_id": user_id, "action": "Delete"}]