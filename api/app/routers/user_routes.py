from fastapi import APIRouter, Response
from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_snake, to_camel

from ..auth.auth import Auth
from ..models.user_model import User

router = APIRouter(
    prefix='/api/users',
    responses={404: {'description': 'Not found'}},
)

class UserIn(BaseModel):
    user_id: int | None = None
    first_name: str
    last_name: str
    user_email: str
    middle_name: str | None = None
    username: str | None = None
    password: str | None = None
    admin: bool | None = None
    viewer: bool | None = None
    chart_builder: bool | None = None
    dash_builder: bool | None = None
    connections: bool | None = None
    
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=to_snake,
            validation_alias=to_camel
        ),
        json_schema_extra= {
            'examples': [
                {
                    'firstName': 'John',
                    'middleName': 'Smith',
                    'lastName': 'Doe',
                    'username': 'jsdoe',
                    'userEmail': 'jdoe@mail.com',
                    'password': 'Plaintext password for a new user',
                    'admin': 'Boolean. Default: False',
                    'viewer': 'Boolean. Default: False',
                    'chartBuilder': 'Boolean. Default: False',
                    'dashBuilder': 'Boolean. Default: False',
                    'connections': 'Boolean. Default: False',
                }
            ]
        }
    )

class UserOut(BaseModel):
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
    admin: bool | None = False
    viewer: bool | None = False
    chartBuilder: bool | None = False
    dashBuilder: bool | None = False
    connections: bool | None = False

@router.get('/')
async def read_users():
    data = User.get_users()
    data = [UserOut(**user).model_dump() for user in data]
    return data

@router.get('/{user_id}')
async def read_user(user_id):
    data = User.get_user(user_id)[0]
    data = UserOut(**data)
    return data.model_dump()

@router.post('/', status_code=201)
async def create_user(user: UserIn, response: Response):
    if not user.password:
        user.password = f'{user.first_name}.{user.last_name}'
    user.password = Auth.generate_password(user.password)
    data = User.create_user(user.model_dump(exclude_none=True))
    return user.model_dump()

@router.put('/{user_id}')
async def update_user(user: UserIn, response: Response):
    if user.password:
        user.password = Auth.generate_password(user.password)
    data = User.update_user(user.model_dump(exclude_none=True))
    return [{'action': f'Updating user {user.user_id}'}]

@router.delete('/{user_id}')
async def delete_user(user_id):
    data = User.delete_user(user_id)
    return [{'user_id': user_id, 'action': 'Delete'}]
