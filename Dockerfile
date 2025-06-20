# Указываем базовый образ
FROM python:3.12
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONPATH=/app

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл с зависимостями и устанавливаем их
RUN pip install poetry
COPY ./backend/pyproject.toml ./
RUN poetry install --no-root

COPY . .

COPY ./start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start


EXPOSE 8000