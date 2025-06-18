
from passlib.context import CryptContext


"""
Здесь функции хеширования паролей,
создания и расшифровки токенов,
функция получения текущего пользователя 
"""

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Функция для создания хэша пароля:
    """
    return pwd_context.hash(password)

print(get_password_hash("546456546"))
print(get_password_hash("546456546"))
print(get_password_hash("546456546"))
print(get_password_hash("546456546"))