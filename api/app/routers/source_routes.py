from fastapi import APIRouter, Body, Response, status
from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_snake, to_camel
from typing import Annotated, Any, List
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

class SourceIn(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=to_snake,
            validation_alias=to_camel
        )
    )
    source_id: int | None = None
    source_type: str | None = None # 'upload' or 'db'(?)
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

@router.get("/")
async def read_sources():
    data = Source.get_sources()
    data = [SourceOut(**source).model_dump() for source in data]
    return data

@router.get("/{source_id}")
async def read_sources(source_id, limit: int | None = None):
    loc_data = Source.get_source(source_id)
    if loc_data['source_type'] == 'upload':
        data = Source.get_data_table(loc_data['source_access_id'], limit)
        return data
    else: # External DB connection
# TODO: Connections phase
# CONNECTIONS PAGE
        pass
    return [{"source_id": source_id}]

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
        Source.create_upload_source(data.user, data.name, table_name)
    except Exception as e:
        print('Error adding entry to sources')
        Source.delete_datatable(table_name)
        response.status_code = status.HTTP_502_BAD_GATEWAY
        return {'error': 'Unable to create resource'}
    return {'created': table_name}

@router.put("/upload/{table_name}", status_code=201)
async def update_source(table_name, data: Annotated[list, Body()], response: Response):
    try:
        success, fails = Source.upload_data(table_name, data)
        return {'rowsAdded': success, 'rowsDropped': fails}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'error': 'Error uploading data'}
    # return [{"action": f'Updating conn {table_name}'}]

@router.delete("/{source_id}")
async def delete_source(source_id):
# CONNECTIONS PAGE
    # Get table
    # Drop table
    # Remove row from data_sources table
    return [{"source_id": source_id, "action": "Delete"}]