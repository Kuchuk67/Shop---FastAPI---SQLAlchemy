import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer
from app.core.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from passlib.context import CryptContext


# --- Database setup ---
DATABASE_URL = "postgresql+asyncpg://postgres:54321@localhost/test1"
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

from app.core.models.users import User

# --- Insert function ---
async def insert_user(user, user2):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            session.add(user)
            session.add(user2)
        await session.commit()
        print(f"Inserted: {user}")
        print(f"Inserted: {user2}")

# --- Create tables and run insert ---
async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    user = User(full_name="admin",
              email= "aaddmmii0@example.com",
              phone="+71234567890",
              password= pwd_context.hash("Qwerty11@"),
              id= 1,
              disabled=False,
              roles="admin")
    user2 = User(full_name="user",
                email="user@example.com",
                phone="+71234567891",
                password=pwd_context.hash("Qwerty11@"),
                id=2,
                disabled=False,
                roles="user")

    await insert_user(user, user2)

if __name__ == "__main__":
    asyncio.run(main())
