import jwt
from datetime import datetime, timedelta, UTC
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Dict
from config import setting

from passlib.context import CryptContext



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password: str) -> str:
    '''
    Функция для создания хэша пароля:
    '''
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    '''
    Функция для проверки пароля
    '''
    return pwd_context.verify(plain_password, hashed_password)



# OAuth2PasswordBearer извлекает токен из заголовка "Authorization: Bearer <token>"
# Параметр tokenUrl указывает маршрут, по которому клиенты смогут получить токен
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# В реальной практике генерируйте ключ, например, с помощью 'openssl rand -hex 32',
#  и храните его в безопасности
#ALGORITHM = "HS256"
 # Время жизни токена

# Функция для создания JWT токена с заданным временем жизни
def create_jwt_token(data: Dict, expires_delta: timedelta):
    """
    Функция для создания JWT токена. Мы копируем входные данные,
    добавляем время истечения и кодируем токен.
    """
    to_encode = data.copy()
    
    # expire time of the token
    expire = datetime.now(UTC) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, 
                             setting.SECRET_KEY,
                             algorithm=setting.ALGORITHM
                             )
    
    # return the generated token
    return encoded_jwt


# Функция для получения пользователя из токена
def get_user_from_token(token: str = Depends(oauth2_scheme)):
    """
    Функция для извлечения информации о пользователе из токена.
    Проверяем токен и извлекаем утверждение о пользователе.
    """
    try:
        payload = jwt.decode(token, 
                             setting.SECRET_KEY,
                             algorithms=[setting.ALGORITHM]
                             ) 
         # Декодируем токен с помощью секретного ключа
        return payload.get("sub") 
     # Возвращаем утверждение о пользователе (subject) из полезной нагрузки
    except jwt.ExpiredSignatureError:
        pass  # Обработка ошибки истечения срока действия токена
    except jwt.InvalidTokenError:
        pass  # Обработка ошибки недействительного токена