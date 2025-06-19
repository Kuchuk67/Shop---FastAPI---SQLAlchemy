from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.core.models.base import Base
from app.core.models.db_helper import db_helper
from app.shopcase.view import router_cart, router_shop
from app.users.views import router as user_router
from app.users.views import router_authentication as user_router_authentication

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
app.include_router(router_shop)
app.include_router(router_cart)


@app.get("/")
async def root(request: Request):
    """тут провто отдает Hello World"""
    return {"message": "Hello World"}
