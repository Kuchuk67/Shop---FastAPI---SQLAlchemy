from .base import Base
from sqlalchemy.orm import Mapped

class User(Base):
    full_name: Mapped[str]
    email: Mapped[str]
    phone: Mapped[int]
    password: Mapped[str]
    password:  Mapped[str]
    