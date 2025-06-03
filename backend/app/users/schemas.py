from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserBase(BaseModel):
    """
    Описывает модель
    """
    full_name: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    phone: int


class User(UserBase):
    """
    Описывает модель 
    """
    password: str
    disabled: bool = False
    roles: str = 'user' # Список ролей пользователя


class UserGet(User):
    """
    Получить данные по пользователю
    """
    id: int

    model_config = ConfigDict(from_attributes=True)



class LoginUser(BaseModel):
    """
    Описывает модель запроса чтоб залогинится
    """
    username: str = Field(..., min_length=3, max_length=20)
    password: str


class UserCreate(UserBase):
    password: str
    #disabled: bool = False
    #roles: str = 'user'