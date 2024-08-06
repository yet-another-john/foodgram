
# Продуктовый помощник Foodgram

Проект «Фудграм» — сайт, на котором пользователи публикуют свои рецепты, добавляют чужие рецепты в избранное и подписываються на публикации других авторов. Зарегистрированным пользователям доступен сервис «Список покупок». Он позволяет создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

### Ссылка на сайт

foodgram-yandex.zapto.org

/admin:
stoliarovea@mail.ru
lenovolenovo

### Авторы:

Евгений

### Стэк:

Python, Django, Django REST framework, Docker, Git Actions

### Необходимые переменные окружения:

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_NAME=
DB_HOST=
DB_PORT=
SECRET_KEY=

### Как запустить проект:

Установить зависимости:
```
pip install -r requirements.txt
```
Запустить Docker Compose:
```
docker compose up
```
Выполнить миграции, заполнить ингредиенты и собрать статические файлы бэкенда:
```
docker compose exec backend python manage.py migrate
```
```
docker compose exec backend python manage.py import_csv ingredients.csv
```
```
docker compose exec backend python manage.py collectstatic
```
```
docker compose exec backend cp -r /app/collected_static/. /backend_static/static/
```
