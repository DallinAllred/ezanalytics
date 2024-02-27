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
    # return [{"dash_name": "Rick"}, {"dashname": "Morty"}]

@router.get("/{dash_id}")
async def read_dashs(dash_id):
    dash_id = ObjectId(dash_id)
    return [{"dash_id": dash_id}]

@router.post("/")
async def create_dash(dash: DashIn):
    return [{"action": "Adding dash"}]

@router.put("/{dash_id}")
async def update_dash(dash_id):
    dash_id = ObjectId(dash_id)
    return [{"action": f'Updating dash {dash_id}'}]

@router.delete("/{dash_id}")
async def delete_dash(dash_id):
    return [{"dash_id": dash_id, "action": "Delete"}]