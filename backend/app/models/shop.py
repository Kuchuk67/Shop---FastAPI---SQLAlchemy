from .base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone, timedelta

dt_l = datetime.now(timezone(timedelta(hours=3)))

class ProductShop(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    description:  Mapped[str]
    price: Mapped[int] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(default=0, gt=0)
    created_at: Mapped[datetime] = mapped_column(nullable=False,
                                                 default=dt_l)
    updated_at: Mapped[datetime] = mapped_column(nullable=False,
                                                 default=dt_l)
    is_active: Mapped[bool] = mapped_column(default=False)


class Сart(Base):
    user_id: Mapped[int] =  mapped_column(ForeignKey('users.id'),
                                          nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('productshops.id'),
                                            nullable=False)
    price: Mapped[int] = mapped_column(nullable=False, gt=0)
    quantity: Mapped[str] = mapped_column(default=1, gt=0)
    
