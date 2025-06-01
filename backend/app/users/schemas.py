from pydantic import BaseModel, ConfigDict, EmailStr, Field


class User(BaseModel):
    """
    Описывает модель 
    """
    full_name: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    phone: int
    password: str
    disabled: bool = False
    roles: tuple[str] = ('user',) # Список ролей пользователя


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