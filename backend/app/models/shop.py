from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone, timedelta

dt_l = datetime.now(timezone(timedelta(hours=3)))

class ProductShop(Base):
    

    name: Mapped[str] = mapped_column(nullable=False)
    description:  Mapped[str]
    price: Mapped[int] = mapped_column(nullable=False)
    quantity: Mapped[str] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(nullable=False,
                                                 default=dt_l)
    updated_at: Mapped[datetime] = mapped_column(nullable=False,
                                                 default=dt_l)
    is_active: Mapped[bool] = mapped_column(default=False)


class Сart(Base):
    

    user_id: Mapped[int] = mapped_column(nullable=False)
    product_id: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    

    name: Mapped[str] = mapped_column(nullable=False)
    description:  Mapped[str]
    price: Mapped[int] = mapped_column(nullable=False)
    quantity: Mapped[str] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(nullable=False,
                                                 default=dt_l)
    updated_at: Mapped[datetime] = mapped_column(nullable=False,
                                                 default=dt_l)
    is_active: Mapped[bool] = mapped_column(default=False)

