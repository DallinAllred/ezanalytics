from fastapi import APIRouter, Body, Response, status
from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_snake, to_camel
from typing import Annotated, Any, List
from enum import Enum

from ..models import source_model

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

# class Column(BaseModel):
#     name: str
#     code: str

class UploadMetadata(BaseModel):
    name: str
    columns: dict
    # columns: List[Column]
    # data: List[Any]

@router.get("/")
async def read_sources():
    data = source_model.Source.get_sources()
    data = [SourceOut(**source).model_dump() for source in data]
    return data

@router.get("/{source_id}")
async def read_sources(source_id, limit: int | None = None):
    loc_data = source_model.Source.get_source(source_id)
    if loc_data['source_type'] == 'upload':
        # Uploaded data, pull from access_id table
        data = source_model.Source.get_data_table(loc_data['source_access_id'], limit)
        return data
    else: # External DB connection
# TODO: Connections phase
        pass
    return [{"source_id": source_id}]

# @router.post("/upload")
# async def create_source():
#     return [{"action": "Adding conn"}]
@router.post("/upload")
# async def create_source(data: Annotated[dict, Body()]):
async def create_source(data: UploadMetadata):
    if len(data.columns) < 1:
        return [{'Error': 'Invalid number of columns supplied'}]
    try:
        table_created = source_model.Source.create_datatable(data.name, data.columns)
    except Exception as e:
        return
    # print(table_created)
    # result = source_model.Source.upload_data(data)
    return [{"action": "Adding conn"}]

@router.put("/{source_id}")
async def update_source(source_id):
    return [{"action": f'Updating conn {source_id}'}]

@router.delete("/{source_id}")
async def delete_source(source_id):
    return [{"source_id": source_id, "action": "Delete"}]