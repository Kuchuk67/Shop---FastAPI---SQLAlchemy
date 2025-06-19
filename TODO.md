# Install

## Docker

Проект находится под системой управления и контеризации - **Docker**.
Если у вас нет Docker - вы можете установить его
с официального сайта: [Docker](https://www.docker.com/get-started/)


## Enviroments

Необходимо заполнить **env_example** и в последствии 
переименовать его в **.env**

```python
POSTGRES_USER=имя пользователя БД
POSTGRES_DB=имя БД
POSTGRES_PASSWORD=пароль
```

## Start
Необходимо ввести команды:
```bash
docker compose up
```

API-cервис будет доступен по адресу:
[127.0.0.1:8000/api/v1](http://127.0.0.1:8000/api/v1)
Документация API
[127.0.0.1:8000/api/v1/docs](http://127.0.0.1:8000/api/v1/docs)

## Testing
Для тестирования нужно перейти внутрь контейнера.

- Найдите контейнер:

```bash
docker ps
```

Ищите контейнер с именем приложения и возьмите
первые 3 символа CONTAITER ID

- Войдите в контейнер:

```bash
docker exec -it YourCONTAINERID bash
```

- Запустите тест

После этого вы попадете внутрь контейнера  
и можете стандартно запускать тесты внутри контейнера

```bash
pytest
```

## Демо данные
Установка производится автоматом
на пересобранные контейнеры и пустую БД

Усли демоданные не нужны - убрать строку \
python demo_data.py\ 
из файла start

### Данные для демо-доступа:
логин email или телефон\
email: admin@example.com\
phone: +71234567890\
password: Qwerty11@

логин email или телефон\
email: user@example.com\
phone: +71234567891\
password: Qwerty11@


