from fastapi import APIRouter, Response, status
from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_snake, to_camel

from bson import ObjectId

from ..models.dash_model import Dashboard

router = APIRouter(
    prefix="/api/dashboards",
    responses={404: {"description": "Not found"}},
)

class DashIn(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=to_snake,
            validation_alias=to_camel
        )
    )
    dash_id: str | None = None
    title: str
    owner: str
    layout: list[list]

@router.get("/")
async def read_dashs():
    data = Dashboard.get_dashboards()
    return data

@router.get("/{dash_id}")
async def read_dashs(dash_id):
    print(dash_id)
    dash_id = ObjectId(dash_id)
    data = Dashboard.get_dash(dash_id)
    return data

@router.post("/")
async def create_dash(dash: DashIn):
    dash = dash.model_dump()
    print(dash)
    del dash['dash_id']
    data = Dashboard.create_dash(dash)
    return [{"action": "Adding dash"}]

@router.put("/{dash_id}")
async def update_dash(dash_id):
    dash_id = ObjectId(dash_id)
    return [{"action": f'Updating dash {dash_id}'}]

@router.delete("/{dash_id}")
async def delete_dash(dash_id):
    dash_id = ObjectId(dash_id)
    data = Dashboard.delete_dash(dash_id)
    return [{"dash_id": str(dash_id), "action": "Delete"}]