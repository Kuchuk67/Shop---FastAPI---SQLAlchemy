from pydantic import BaseModel, computed_field, Field


class CommonHeaders(BaseModel):
    """
    Описывает модель заголовка запроса
    """
    headers: object

    @computed_field
    def user_agent(self) -> str:
        user_agent: str = Field(self.headers.get('user-agent'), min_length=180, max_length=500)
        return user_agent

    @computed_field
    def accept_language(self) -> str:
        return self.headers.get('accept-language')

# headers = CommonHeaders(headers=request.headers)
