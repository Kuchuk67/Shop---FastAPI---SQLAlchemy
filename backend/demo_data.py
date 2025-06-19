import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.models.base import Base
from passlib.context import CryptContext
import random
from app.core.models.users import User
from app.core.models.shop import ProductShop, Cart
from config import setting as set

# --- Database setup ---
DATABASE_URL = f"postgresql+asyncpg://{set.POSTGRES_USER}:{set.POSTGRES_PASSWORD}@{set.POSTGRES_HOST}:{set.POSTGRES_PORT}/{set.POSTGRES_DB}"
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine,
                                 class_=AsyncSession,
                                 expire_on_commit=False)


# --- Insert function ---
async def insert_user(user, user2, product, cart):

    try:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                session.add(user)
                session.add(user2)
                await session.commit()
    except:
        print("Демо-данные в БД не добавлены")
    else:
        async with AsyncSessionLocal() as session:
            async with session.begin():

                # добавим товары
                for item in product:
                    session.add(item)
                await session.commit()

        async with AsyncSessionLocal() as session:
            async with session.begin():

                # добавим товары
                for item in cart:
                    session.add(item)
                await session.commit()

    

# --- Create tables and run insert ---
async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    user = User(full_name="admin",
              email= "admin@example.com",
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
    cart=[]
    cart.append(Cart(quantity=15,product_id=2,user_id=2,price=10))
    cart.append(Cart(quantity=3,product_id=1,user_id=2,price=25))
    cart.append(Cart(quantity=28,product_id=5,user_id=2,price=5))
    cart.append(Cart(quantity=55,product_id=1,user_id=2,price=1))
    cart.append(Cart(quantity=10,product_id=1,user_id=1,price=100))
    product = []
    for x in range(1, 500):
            prod_data = ProductShop(
                name=f"Товар {x}",
                description=f"Описание: {x}, подробное описание товара",
                price=int(random.random()*100000),
                quantity=int(random.random()*100),
                is_active=True
            )
            # print("*******  ",prod_data)
            product.append(prod_data)

    await insert_user(user, user2, product, cart)

if __name__ == "__main__":
    asyncio.run(main())


