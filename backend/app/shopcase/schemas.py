from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone, timedelta


class ProductShop(BaseModel):
    """
    Описывает базовую модель
    """

    name: str = Field(..., min_length=6, max_length=30)
    description: str = Field(..., max_length=30)
    price: int = Field(default=0, gt=0)
    quantity: int = Field(default=0, gt=0)
    created_at: datetime = Field(
        default=datetime.now(timezone(timedelta(hours=3)))
    )
    updated_at: datetime = Field(
        default=datetime.now(timezone(timedelta(hours=3)))
    )
    is_active: bool = True


class ProductShopGet(ProductShop):
    """
    Получить данные по продукту,
    """

    id: int
    model_config = ConfigDict(from_attributes=True)


class Cart(BaseModel):
    """
    Описывает базовую модель
    """

    user_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    price: int = Field(gt=0)
    quantity: int = Field(gt=0)


class CartGet(Cart):
    """
    Получить данные по корзине,
    """

    id: int
    model_config = ConfigDict(from_attributes=True)
