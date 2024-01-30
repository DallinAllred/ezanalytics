from fastapi import APIRouter

router = APIRouter(
    prefix="/connections",
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_conns():
    return [{"conn_name": "Rick"}, {"connname": "Morty"}]

@router.get("/{conn_id}")
async def read_conns(conn_id):
    return [{"conn_id": conn_id}]

@router.post("/")
async def create_conn():
    return [{"action": "Adding conn"}]

@router.put("/{conn_id}")
async def update_conn(conn_id):
    return [{"action": f'Updating conn {conn_id}'}]

@router.delete("/{conn_id}")
async def delete_conn(conn_id):
    return [{"conn_id": conn_id, "action": "Delete"}]