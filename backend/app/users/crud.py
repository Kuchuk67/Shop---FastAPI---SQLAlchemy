from app.users.schemas import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models import User
from sqlalchemy import select
from sqlalchemy.engine import Result

# def create_user2(user_in: User):
#     user = user_in.model_dump()
#     return {
#         "success": True,
#         "user": user,
#     }

async def get_user(session: AsyncSession) -> tuple[User] | None:
    #user = User(**user_in.model_dump())
    stmt=select(User)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return tuple(users)
