from fastapi import FastAPI
from app.core.db import init_db
from contextlib import asynccontextmanager

from app.models.user import User
from app.models.travel import Travel
from app.models.chat import ChatMessages
from app.models.itinerary import Itinerary


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 시 테이블 생성 (이미 있으면 생성 안 함)
    init_db()
    yield

app = FastAPI(title="Voyagent Backend API", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Voyagent Backend API!"}