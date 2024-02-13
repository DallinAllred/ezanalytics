from fastapi import APIRouter, Body, Response, status
from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_snake, to_camel
from typing import Annotated, Any, List

from ..models import source_model

router = APIRouter(
    prefix="/api/sources",
    responses={404: {"description": "Not found"}},
)

class SourceIn(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=to_snake,
            validation_alias=to_camel
        )
    )
    source_id: int | None = None
    source_type: str | None = None
    source_label: str
    source_access_id: str

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
    sourceType: str | None = None
    sourceLabel: str
    sourceAccessId: str

class Column(BaseModel):
    name: str
    type: str

class Upload(BaseModel):
    name: str
    columns: List[Column]
    data: List[Any]

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

@router.post("/upload")
async def create_source(data: Annotated[dict, Body()]):
    table_name = data['name']
    columns = data['columns']
    if len(columns) < 1:
        return [{'Error': 'Invalid number of columns supplied'}]
    try:
        table_created = source_model.Source.create_datatable(table_name, columns)
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