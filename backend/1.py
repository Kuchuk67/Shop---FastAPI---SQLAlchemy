import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String

# --- Database setup ---
DATABASE_URL = "postgresql+asyncpg://postgres:54321@localhost/test1"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# --- Model ---
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)

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

    user = User(name="Alice2", email="alice2@example.com")
    await insert_user(user)

if __name__ == "__main__":
    asyncio.run(main())
