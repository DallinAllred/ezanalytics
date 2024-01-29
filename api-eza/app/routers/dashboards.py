from fastapi import APIRouter

router = APIRouter(
    prefix="/dashboards",
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_dashs():
    return [{"dash_name": "Rick"}, {"dashname": "Morty"}]

@router.get("/{dash_id}")
async def read_dashs(dash_id):
    return [{"dash_id": dash_id}]

@router.post("/")
async def create_dash():
    return [{"action": "Adding dash"}]

@router.put("/{dash_id}")
async def update_dash(dash_id):
    return [{"action": f'Updating dash {dash_id}'}]

@router.delete("/{dash_id}")
async def delete_dash(dash_id):
    return [{"dash_id": dash_id, "action": "Delete"}]