from fastapi import APIRouter, Response, status
from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_snake, to_camel

from ..models import chart_model

router = APIRouter(
    prefix="/api/charts",
    responses={404: {"description": "Not found"}},
)

class Chart(BaseModel):
    chartId: int | None = None
    sourceId: dict
    title: str
    type: dict
    groupBy: str
    data: dict
    options: dict

@router.get("/")
async def read_charts():
    data = chart_model.Chart.get_charts()
    return [{"user_name": "Rick"}, {"username": "Morty"}]

@router.get("/{chart_id}")
async def read_charts(chart_id):
    chart = chart_model.Chart.get_chart(chart_id)
    return [{"chart_id": chart_id}]

@router.post("/")
async def create_chart(chart: Chart):
    print(chart)
    result = chart_model.Chart.create_chart(chart.model_dump())
    print(result)
    return result

@router.put("/{chart_id}")
async def update_chart(chart_id):
    return [{"action": f'Updating chart {chart_id}'}]

@router.delete("/{chart_id}")
async def delete_chart(chart_id):
    return [{"chart_id": chart_id, "action": "Delete"}]