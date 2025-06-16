from .base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User

dt_l: datetime = datetime.now() #timezone(timedelta(hours=3))

class ProductShop(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    description:  Mapped[str] = mapped_column(nullable=True)
    price: Mapped[int] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(nullable=False,
                                                 default=dt_l)
    updated_at: Mapped[datetime] = mapped_column(nullable=False,
                                                 default=dt_l)
    is_active: Mapped[bool] = mapped_column(default=False)


class Cart(Base):
    user_id: Mapped[int] =  mapped_column(ForeignKey('users.id'),
                                          nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('productshops.id'),
                                            nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(default=1)

    user: Mapped["User"] = relationship(back_populates="cart")

    