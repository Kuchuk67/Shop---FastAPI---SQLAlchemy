from datetime import datetime, timedelta, timezone

from pydantic import BaseModel, ConfigDict, Field


class ProductShop(BaseModel):
    """
    Описывает базовую модель
    """

    name: str = Field(..., min_length=3, max_length=30)
    description: str = Field(..., max_length=250)
    price: int = Field(default=0, ge=0)
    quantity: int = Field(default=0, ge=0)
    is_active: bool = True


class ProductShopGet(ProductShop):
    """
    Получить данные по продукту,
    """

    id: int
    created_at: datetime = Field(default=datetime.now(timezone(timedelta(hours=3))))
    updated_at: datetime = Field(default=datetime.now(timezone(timedelta(hours=3))))
    model_config = ConfigDict(from_attributes=True)



class ProductShopPut(BaseModel):
    quantity: int = Field(ge=0)
    is_active: bool
    price: int = Field(ge=0)


class CartBase(BaseModel):
    """
    Описывает базовую модель корзины
    """

    quantity: int = Field(gt=0)
    product_id: int = Field(gt=0)


class Cart(CartBase):
    """
    Описывает базовую модель
    """

    user_id: int = Field(gt=0)
    price: int = Field(gt=0)


class CartGet(Cart):
    """
    Получить данные по корзине
    """

    id: int
    products:  ProductShopGet
    model_config = ConfigDict(from_attributes=True)



class CartPatch(CartBase):
    """
    Изменить количество товара в корзине
    """

    id: int
