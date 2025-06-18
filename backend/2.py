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
'''Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    disabled: Mapped[bool] = mapped_column(default=False, nullable=False)
    roles: Mapped[str] = mapped_column(default="user", nullable=False)'''
from app.core.models.users import User

# --- Insert function ---
async def insert_user(user):
    async with AsyncSessionLocal() as session:
        async with session.begin():

            session.add(user)
        await session.commit()
        print(f"Inserted: {user}")

# --- Create tables and run insert ---
async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    user = User(full_name="admin",
              email= "aaddmmii0@example.com",
              phone="+76051357380",
              password= pwd_context.hash("password"),
              id= 13,
              disabled=False,
              roles="admin")

    await insert_user(user)

if __name__ == "__main__":
    asyncio.run(main())
