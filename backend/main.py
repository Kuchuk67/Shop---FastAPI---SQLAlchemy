from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from databases import Database
from pydantic import BaseModel
from app.models.base import Base
from app.models.db_helper import db_helper

from config import setting

# URL для PostgreSQL (ЗАМЕНИТЕ user, password, localhost, dbname на свои реальные данные!)
# DATABASE_URL = "postgresql://postgres:54321@localhost/shop"

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield



app = FastAPI(lifespan=lifespan)
#print(type(setting.DEBAG))