from fastapi import APIRouter
from ..models import user_model
from pydantic import BaseModel, alias_generators, ConfigDict
from pydantic.alias_generators import to_snake, to_camel
# from fastapi_camelcase import CamelModel

router = APIRouter(
    prefix='/users',
    responses={404: {'description': 'Not found'}},
)

class User(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    first_name: str
    last_name: str
    user_email: str
    middle_name: str | None = None
    username: str | None = None
    password: str | None = None
    admin: bool | None = False
    viewer: bool | None = False
    chart_builder: bool | None = False
    dash_builder: bool | None = False
    connections: bool | None = False

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'firstName': 'John',
                    'middleName': 'Smith',
                    'lastName': 'Doe',
                    'username': 'jsdoe',
                    'userEmail': 'jdoe@mail.com',
                    'password': 'Password hash or plaintext password for a new user',
                    'admin': 'Boolean. Default: False',
                    'viewer': 'Boolean. Default: False',
                    'chartBuilder': 'Boolean. Default: False',
                    'dashBuilder': 'Boolean. Default: False',
                    'connections': 'Boolean. Default: False',
                }
            ]
        }
    }


@router.get('/')
async def read_users():
    data = user_model.User.get_users()
    # user = User(**data)
    return data

@router.get('/{user_id}')
async def read_user(user_id):
    data = user_model.User.get_user(user_id)
    data = [User(**user).model_dump_json() for user in data]
    return data

@router.post('/')
async def create_user(user: User):
    if not user.password:
        user.password = f'{user.first_name}_{user.last_name}'
    data = user_model.User.create_user(user)
    print(user)
    return [{'action': 'Adding user'}]

@router.put('/{user_id}')
async def update_user(user_id):
    return [{'action': f'Updating user {user_id}'}]

@router.delete('/{user_id}')
async def delete_user(user_id):
    return [{'user_id': user_id, 'action': 'Delete'}]