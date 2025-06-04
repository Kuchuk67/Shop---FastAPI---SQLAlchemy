from contextlib import nullcontext
from lib2to3.pgen2.tokenize import blank_re

from pydantic import BaseModel, ConfigDict, EmailStr, Field, constr

class UserBase(BaseModel):
    """
    Описывает базовую модель
    """
    full_name: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    phone: int


class User(UserBase):
    """
    Описывает полную модель,
    но без пароля и ID
    """
    disabled: bool = False
    roles: str = 'user' # Список ролей пользователя


class UserGet(User):
    """
    Получить данные по пользователю,
    но без пароля
    """
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserPass(UserGet):
    """
    Полная модель Пользователя
    """
    password: str


class UserCreate(UserBase):
    """
    Модель для создания Пользователя
    """
    password: str


class LoginUser(BaseModel):
    """
    Описывает модель запроса чтоб залогинится
    login: email пользователя или телефон +7..........
    """
    login: EmailStr | constr(pattern=r"\+7[0-9]{10}")
    password: str



