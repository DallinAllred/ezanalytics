from fastapi import APIRouter, Response, status
from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_snake, to_camel

from bson import ObjectId

from ..models import chart_model

router = APIRouter(
    prefix="/api/charts",
    responses={404: {"description": "Not found"}},
)

class Chart(BaseModel):
    chartId: str | None = None
    sourceId: dict
    title: str
    type: dict
    groupBy: str | None = None
    data: dict
    options: dict

@router.get("/")
async def read_charts():
    data = chart_model.Chart.get_charts()
    return data

@router.get("/{chart_id}")
async def read_charts(chart_id):
    chart_id = ObjectId(chart_id)
    chart = chart_model.Chart.get_chart(chart_id)
    return chart

@router.post("/")
async def create_chart(chart: Chart):
    result = chart_model.Chart.create_chart(chart.model_dump(exclude_none=True))
    return result

@router.put("/{chart_id}")
async def update_chart(chart_id):
    return [{"action": f'Updating chart {chart_id}'}]

@router.delete("/{chart_id}")
async def delete_chart(chart_id):
    result = chart_model.Chart.delete_chart(ObjectId(chart_id))
    return [{"chart_id": chart_id, "action": "Delete"}]