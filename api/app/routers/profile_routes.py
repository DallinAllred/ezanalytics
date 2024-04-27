from argon2.exceptions import VerificationError
from fastapi import APIRouter, Body, Cookie, Response, status
from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_snake, to_camel
from typing import Annotated, Any

from ..auth.auth import Auth
from ..models.user_model import User

router = APIRouter(
    prefix='/api/profile',
    responses={404: {'description': 'Not found'}},
)

class ProfileIn(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=to_snake,
            validation_alias=to_camel
        )
    )
    user_id: int | None = None
    first_name: str
    last_name: str
    user_email: str
    middle_name: str | None = None
    username: str | None = None

class ProfileOut(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=to_camel,
            validation_alias=to_snake
        ),
        extra='ignore',
        populate_by_name=True,
        from_attributes=True
    )
    userId: int
    firstName: str
    lastName: str
    userEmail: str
    middleName: str | None = None
    username: str | None = None

@router.get('/{user_id}')
async def read_user(user_id, response: Response):
    try:
        data = User.get_user(user_id)[0]
        data = ProfileOut(**data)
        return data.model_dump()
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return

@router.put('/password/{user_id}')
async def update_password(user_id,
                          response: Response,
                          passwords: Annotated[dict, Body()] = None,
                          session_id: Annotated[Any, Cookie()] = None):
    session_user = Auth.get_permissions(session_id)
    session_user = session_user['user_id']
    if user_id != session_user:
        response.status_code = status.HTTP_403_FORBIDDEN
        return
    old = passwords['oldPassword']
    proposed = passwords['newPassword']
    try:
        Auth.validate_password(user_id, old)
        new_hash = Auth.generate_password(proposed)
        Auth.update_password(user_id, new_hash)
    except VerificationError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return

@router.put('/{user_id}')
async def update_user(user_id,
                      user: ProfileIn,
                      response: Response,
                      session_id: Annotated[Any, Cookie()] = None):
    session_user = Auth.get_permissions(session_id)
    session_user = session_user['user_id']
    if user_id != session_user:
        response.status_code = status.HTTP_403_FORBIDDEN
        return
    print(user.model_dump(exclude_none=True))
    try:
        data = User.update_user(user.model_dump(exclude_none=True))
        return [{'action': f'Updating user {user.user_id}'}]
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return
