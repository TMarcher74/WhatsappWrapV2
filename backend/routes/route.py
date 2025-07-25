from fastapi import APIRouter

route = APIRouter()

@route.get("upload")
async def upload():
    pass