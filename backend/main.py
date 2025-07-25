from fastapi import FastAPI, APIRouter
from routes import route

app = FastAPI()
app.include_router(route)