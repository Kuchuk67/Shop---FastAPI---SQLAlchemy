from fastapi import HTTPException, status
from functools import wraps


class PermissionRole:
    """
    Декоратор для проверки ролей пользователя
    пример:
    @PermissionRole(["admin", "user"])
    async def get_user(current_user: UserGet = Depends(get_current_user))
    """

    def __init__(self, roles: list[str]):
        self.roles = roles  # Список разрешённых ролей

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = kwargs.get("current_user")  # Получаем текущего пользователя

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Требуется аутентификация",
                )

            if user.roles == "admin":  # Админ всегда имеет доступ ко всему
                return await func(*args, **kwargs)

            if (
                user.roles not in self.roles
            ):  # not any(role in user.roles for role in self.roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Недостаточно прав для доступа",
                )
            return await func(*args, **kwargs)

        return wrapper
