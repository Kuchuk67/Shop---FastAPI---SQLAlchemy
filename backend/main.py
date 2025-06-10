from fastapi import FastAPI, HTTPException, Request
from contextlib import asynccontextmanager

from app.core.models.base import Base
from app.core.models.db_helper import db_helper


from config import setting
from app.core.headers import CommonHeaders
from app.users.views import router as user_router, router_authentication as user_router_authentication

# URL для PostgreSQL (ЗАМЕНИТЕ user, password, localhost, dbname на свои реальные данные!)
# DATABASE_URL = "postgresql://postgres:54321@localhost/shop"

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield



app = FastAPI(lifespan=lifespan)

# подключаем дополнительные роуторы - views
app.include_router(user_router)
app.include_router(user_router_authentication)


@app.get("/")
async def root(request: Request):
    """ тут провто отдает Hello World """
    return {"message": "Hello World"}