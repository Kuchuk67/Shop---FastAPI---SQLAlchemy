from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """
    Описывает базовую модель
    """

    full_name: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    phone: str = Field(pattern=r"\+7[0-9]{10}")


class User(UserBase):
    """
    Описывает полную модель,
    но без пароля и ID
    """

    disabled: bool = False
    roles: str = "user"  # Список ролей пользователя


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

    password: str = Field(..., min_length=8)
    password_2: str = Field(..., min_length=8)
    # ^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).*$
    # (?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,}$

class LoginUser(BaseModel):
    """
    Описывает модель запроса чтоб залогинится
    login: email пользователя или телефон +7..........
    """
    # login может быть телефоном или email
    login: str = Field(..., pattern=r"\+7[0-9]{10}|^\S+@\S+\.\S+$")
    password: str


class UserPatch(BaseModel):
    disabled: bool | None
    roles: str | None

