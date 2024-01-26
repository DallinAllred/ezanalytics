from fastapi import APIRouter

router = APIRouter(
    prefix="/charts",
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_charts():
    return [{"user_name": "Rick"}, {"username": "Morty"}]

@router.get("/{chart_id}")
async def read_charts(chart_id):
    return [{"chart_id": chart_id}]

@router.post("/")
async def create_chart():
    return [{"action": "Adding chart"}]

@router.put("/{chart_id}")
async def update_chart(chart_id):
    return [{"action": f'Updating chart {chart_id}'}]

@router.delete("/{chart_id}")
async def delete_chart(chart_id):
    return [{"chart_id": chart_id, "action": "Delete"}]