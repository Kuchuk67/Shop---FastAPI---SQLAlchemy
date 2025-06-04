from .base import Base
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    full_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    disabled: Mapped[bool] = mapped_column(default=False, nullable=False)
    roles: Mapped[str] = mapped_column(default="user", nullable=False)
