Кейс от Mediasoft
---
* **Фамилия Имя:** Умывалкин Максим
* **Тестовое задание:** Реализовать сервис, который принимает и отвечает на HTTP запросы
* **Описание проекта:** 
* **Подготовительные действия**
  1. Создать .env файл в корне проекта со следующим содержимым (заполнить соответственно)
```dotenv
DB_NAME=""
DB_USER=""
DB_PASSWORD=""
DB_HOST=""
DB_PORT=""
SECRET_KEY=""
```
* **Информация о доступах:** -
* **Запуск проекта**
  * Ручной запуск
    * Установить [python 3.10.4](https://www.python.org/downloads/)
    * Установить [postgresql 14.3](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
    * Создать базу данных в postgres
    * Создать и заполнить .env.dev файл
    * Выполнить последовательно команды
```pycon
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
  * Docker
```docker
docker-compose --env-file .env.dev --file docker-compose.yml up -d
```
  * Docker новой версии
```docker
docker compose --env-file .env.dev --file docker-compose.yml up -d
```
---
### Работа с запросами
* Любой запрос начинается с префикса /api/v1, дальше всё по ТЗ
* Список endpoint`ов
  * `GET /api/v1/city/`
  * `GET /api/v1/city/id/`
  * `GET /api/v1/city/id/street/`
  * `POST /api/v1/city/`
  * `PATCH /api/v1/city/id/`
  * `DELETE /api/v1/city/id/`
  * ##############################
  * `GET /api/v1/street/`
  * `GET /api/v1/street/id/`
  * `POST /api/v1/street/`
  * `PATCH /api/v1/street/id/`
  * `DELETE /api/v1/street/id/`
  * ##############################
  * `GET /api/v1/shop/`
  * `GET /api/v1/shop/id/`
  * `POST /api/v1/shop/`
  * `PATCH /api/v1/shop/id/`
  * `DELETE /api/v1/shop/id/`
* Возможные query параметры
  * У всех доступен `?ordered_by=id/-id`. id - по возрастанию id, -id - по убыванию
  * У shop по мимо сортировки доступны `?street=...`, `?city=...`, `?open=...`. Могут применяться в любой комбинации.
---
### POST запросы. Примеры
* `/api/v1/city/`
```json
{
    "name": "Ульяновск"
}
```
* `/api/v1/street/` Для указания города используется id города
```json
{
    "name": "ASd",
    "city": 1
}
```
* `/api/v1/shop/` Если у города нет улицы, которая указана в запросе, вернётся 400 статус код
```json
{
    "name": "qwe",
    "house": "10/b",
    "open_time": "10:00",
    "close_time": "4:14",
    "city": 2,
    "street": 4
}
```
---
### GET запросы. Примеры
* `/api/v1/city/`
```json
[
    {
        "id": 2,
        "name": "Ульяновск"
    },
    {
        "id": 3,
        "name": "Москва"
    },
    {
        "id": 15,
        "name": "Qwe"
    }
]
```
* `/api/v1/city/2/street/?ordered_by=-id` (по убыванию id)
```json
[
    {
        "id": 7,
        "city": {
            "id": 2,
            "name": "Ульяновск"
        },
        "name": "Qqqqqqqq"
    },
    {
        "id": 5,
        "city": {
            "id": 2,
            "name": "Ульяновск"
        },
        "name": "Тимирязева"
    },
    {
        "id": 4,
        "city": {
            "id": 2,
            "name": "Ульяновск"
        },
        "name": "Тимирязева"
    }
]
```
* `/api/v1/shop/?city=Ульяновск&ordered_by=-id&open=1` (в рамках ТЗ можно добавлять и удалять параметры из запросы)
  * P.S.: запускалось в 10:44, поэтому при open=1 вернулись эти данные
```json
[
    {
        "id": 17,
        "city": {
            "id": 2,
            "name": "Ульяновск"
        },
        "street": {
            "id": 4,
            "city": {
                "id": 2,
                "name": "Ульяновск"
            },
            "name": "Тимирязева"
        },
        "name": "qwe",
        "house": "10/b",
        "open_time": "10:00:00",
        "close_time": "04:14:00"
    },
    {
        "id": 6,
        "city": {
            "id": 2,
            "name": "Ульяновск"
        },
        "street": {
            "id": 4,
            "city": {
                "id": 2,
                "name": "Ульяновск"
            },
            "name": "Тимирязева"
        },
        "name": "qq123",
        "house": "123",
        "open_time": "02:00:00",
        "close_time": "22:00:00"
    },
    {
        "id": 5,
        "city": {
            "id": 2,
            "name": "Ульяновск"
        },
        "street": {
            "id": 5,
            "city": {
                "id": 2,
                "name": "Ульяновск"
            },
            "name": "Тимирязева"
        },
        "name": "аываыва",
        "house": "123",
        "open_time": "10:00:00",
        "close_time": "22:00:00"
    }
]
```
---
### PATCH запросы. Примеры
* `/api/v1/shop/1/`
```json
{
    // Request
    "name": "Крутятся пластинки",
    "street": 4
}
```
```json
{
    // Response
    "id": 1,
    "city": {
        "id": 2,
        "name": "Ульяновск"
    },
    "street": {
        "id": 4,
        "city": {
            "id": 2,
            "name": "Ульяновск"
        },
        "name": "Тимирязева"
    },
    "name": "Крутятся пластинки",
    "house": "11/qwe",
    "open_time": "17:37:00",
    "close_time": "18:35:00"
}
```