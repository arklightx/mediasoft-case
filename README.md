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
```python
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
  * Docker
    * TBD