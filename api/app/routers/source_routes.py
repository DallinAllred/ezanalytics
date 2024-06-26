from fastapi import APIRouter, Body, Response, status
from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_snake, to_camel
from typing import Annotated
from enum import Enum

from ..models.source_model import Source

router = APIRouter(
    prefix="/api/sources",
    responses={404: {"description": "Not found"}},
)

class ColEnum(str, Enum):
    numeric = 'NUMERIC'
    varchar = 'VARCHAR'
    timestamp = 'TIMESTAMP'

class EngineEnum(str, Enum):
    mariadb = 'mariadb'
    mysql = 'mysql'
    postgres = 'postgres'

class SourceIn(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=to_snake,
            validation_alias=to_camel
        )
    )
    source_id: int | None = None
    source_type: str | None = None # 'upload' or 'external'(?)
    source_label: str # Human readable label
    source_access_id: str # Table name in Postgres

class SourceOut(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=to_camel,
            validation_alias=to_snake
        ),
        extra='ignore',
        populate_by_name=True,
        from_attributes=True
    )
    sourceId: int | None = None
    sourceType: str = 'upload'
    sourceLabel: str
    sourceAccessId: str

class UploadMetadata(BaseModel):
    columns: dict
    name: str
    user: int

class ConnectionData(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=to_snake,
            validation_alias=to_camel
        )
    )
    source_id: int | None = None
    user: int
    name: str
    engine: str
    db_host: str
    db_port: int
    database: str
    db_user: str
    db_password: str
    query: str

@router.get("/")
async def read_sources():
    data = Source.get_sources()
    data = [SourceOut(**source).model_dump() for source in data]
    return data

@router.get("/conndetails/{source_id}")
async def read_connection_details(source_id):
    src_data = Source.get_source(source_id)
    data = Source.get_connection_details(src_data['source_access_id'])
    return data

@router.get("/{source_id}")
async def read_source(source_id, response: Response, limit: int | None = None):
    loc_data = Source.get_source(source_id)
    if loc_data['source_type'] == 'upload':
        try:
            data = Source.get_data_table(loc_data['source_access_id'], limit)
            return data
        except Exception as e:
            print(e)
            response.status = status.HTTP_500_INTERNAL_SERVER_ERROR
            return
    else: # External DB connection
        try:
            print('Loading external db')
            data = Source.get_connection_data(loc_data['source_access_id'])
            return data
        except Exception as e:
            print(e)
            print('Error in loading external data')
            response.status = status.HTTP_500_INTERNAL_SERVER_ERROR
            return

@router.post("/upload", status_code=201)
async def create_source(data: UploadMetadata, response: Response):
    if len(data.columns.keys()) < 1:
        print('Invalid column count')
        return {'Error': 'Invalid number of columns supplied'}
    try:
        for col in data.columns.keys():
            col_type = data.columns[col]
            col_type = ColEnum[col_type]
            data.columns[col] = col_type.value
    except ValueError as e:
        print('Invalid column type')
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': 'Invalid column type provided'}
    try:
        table_name, version = Source.create_datatable(data.name, data.columns)
    except Exception as e:
        print('Error creating table')
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'error': 'Unable to create table'}
    try:
        if version > 0:
            data.name = f'{data.name}_{version}'
        Source.create_source(data.user, 'upload', data.name, table_name)
    except Exception as e:
        print('Error adding entry to sources', e)
        Source.delete_datatable(table_name)
        response.status_code = status.HTTP_502_BAD_GATEWAY
        return {'error': 'Unable to create resource'}
    return {'created': table_name}

@router.post("/connection", status_code=201)
async def create_connection(data: ConnectionData, response: Response):
    result = create_new_connection(data)
    if result == 500:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return

@router.put("/upload/{table_name}", status_code=201)
async def update_source(table_name, data: Annotated[list, Body()], response: Response):
    try:
        success, fails = Source.upload_data(table_name, data)
        return {'rowsAdded': success, 'rowsDropped': fails}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'error': 'Error uploading data'}

@router.put("/connection/{source_id}", status_code=201)
async def create_connection(source_id, data: ConnectionData, response: Response):
    Source.delete_source(source_id)
    result = create_new_connection(data)
    if result == 500:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return

@router.delete("/{source_id}")
async def delete_source(source_id, response: Response):
    source_data = Source.get_source(source_id)
    if source_data['source_type'] == 'upload':
        try:
            name = Source.delete_datatable(source_data['source_access_id'])
            id = Source.delete_source(source_id)
            return {'id': id, 'name': name}
        except Exception as e:
            print(e)
            print(f'Unable to delete {source_data['source_access_id']}')
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return
    else:
        try:
            id = Source.delete_source(source_id)
            return {'id': id, 'external': source_data['source_access_id']}
        except Exception as e:
            print(e)
            print(f'Unable to delete {source_data['source_access_id']}')
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return

def create_new_connection(data):
    try:
        eng = EngineEnum(data.engine)
    except ValueError as e:
        print('Unsupported database engine')
        return 500
    
    # Check for duplicate names. Add incremental number if any exist
    existing_sources = Source.get_sources()
    dup_count = 0
    access_id = data.name.lower()
    proposed_id = '_'.join(data.name.lower().split())
    source_ids = [src['source_access_id'] for src in existing_sources]
    while proposed_id in source_ids:
        dup_count += 1
        proposed_id = f'{access_id}_{dup_count}'
    if dup_count > 0:
        data.name = f'{data.name}_{dup_count}'

    # Create the data source entry
    try:
        Source.create_source(data.user, 'external', data.name, proposed_id)
    except Exception as e:
        print(e)
        return 500
    
    # Create the connection entry
    try:
        Source.create_connection(data.model_dump(exclude_none=True), proposed_id)
    except Exception as e:
        print(e)
        return 500