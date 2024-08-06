# foodgram
## Описание проекта.
Проект Foodgram позволяет пользователям оставлять свои рецепты. Можно добавить нужные ингредиенты и прописать количество. Также можно указать время приготовления и приложить фотографию рецепта.
Рецепты можно фильтровать по тегам, такие как «Завтрак», «Обед», «Ужин». Например, в теге «Завтрак» могут быть рецепты «Блинчики» и «Омлет», а под тегом «Обед» — «Борщ», «Котлеты с пюрешкой» и свежий салатик.
Пользователь может подписаться на другого пользователя, чтобы наблюдать за его рецептами, а также может добавить рецепт в избранное или выгрузить список покупок.
В одном рецепте может быть только 1 повторяющийся ингредиент. При этом если добавить в список покупок несколько рецептов с одинаковыми ингредиентами - пользователь получит сводный список нгредиентов.
Добавлять теги и ингредиенты могут только администраторы. Добавлять рецепты могут только аутентифицированные пользователи. При этом просматривать все рецепты у неавторизованных пользователей возможность есть.

Бекенд проекта свзывается с фронтендом через Docker контейнеры, с помощью которых проект можно развернуть на сервере.

## Алгоритм регистрации пользователей.
Пользователь заполняет форму регистрации на добавление нового пользователя с параметрами: email, username, first_name, last_name, password - на эндпоинт `/api/users/`.
Foodgram сохраняет пользователя в базе данных, после чего пользователь отправляет email и password по адресу `/api/auth/token/login`, в ответе на запрос ему приходит token.

## Ресурсы Foodgram.
- Ресурс <span style="color: #7FFFD4">**auth**</span>: аутентификация.
- Ресурс <span style="color: #7FFFD4">**users**</span>: пользователи.
- Ресурс <span style="color: #7FFFD4">**recipes**</span>: рецепты, которые создают пользователи.
- Ресурс <span style="color: #7FFFD4">**ingredients**</span>: ингредиенты для рецептов. К рецепту привязываются через вспомогательную модель <span style="color: #7FFFD4">listingredients</span>.
- Ресурс <span style="color: #7FFFD4">**tags**</span>: теги для рецептов («Завтрак», «Обед», «Ужин»). Одно произведение может быть привязано к нескольким тегам.
- Ресурс <span style="color: #7FFFD4">**favorite**</span>: добавление в избранное. Добавить можно неограниченное количество рецептов. Связывается с рецептами через вспомогательную модель <span style="color: #7FFFD4">listfavorite</span>.
- Ресурс <span style="color: #7FFFD4">**subscribtions**</span>: подписки на пользователей. Подписаться можно только один раз. Связывается с пользователями через вспомогательную модель <span style="color: #7FFFD4">listsubscribtions</span>.
- Ресурс <span style="color: #7FFFD4">**shopping cart**</span>: списки покупок привязанные к рецептам. Пользователь может добавить рецепт в список покупок.
- Ресурс <span style="color: #7FFFD4">**downloads shopping cart**</span>: добавленные в список покупок рецепты - можно выгрузить в виде списка покупок.

> Каждый ресурс описан в документации: указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, когда это необходимо.

## Пользовательские роли и права доступа.
🤷 Аноним — может просматривать все рецепты, фильтровать по тегам, смотреть пользователей.

👀 Аутентифицированный пользователь (user) — может читать всё, как и Аноним, может публиковать рецепты и добавлять в избранное, список покупок, скачивать список покупок. Может редактировать и удалять свои рецепты и списки избранного/покупок. Добавлять теги к рецептам. Эта роль присваивается по умолчанию каждому новому пользователю.

💼 Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять рецепты, ингредиенты, теги. Может назначать роли и права пользователям, заходить в админку проекта.

🦸🏼‍♂️ Суперпользователь Django должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперпользователя — это не лишит его прав администратора. Суперпользователь — всегда администратор, но администратор — не обязательно суперпользователь.

---
## <h2 id="instruct">Инструкция по запуску.</h2>
### Скопируйте на серсер файл с данными .env.
### Деплой через docker-compose.prodaction.yml срабатывает автоматически после команды "git push" в main ветку.
---

## Информация об авторах.
Бэкенд написан студентом: [litanchick](https://github.com/litanchick).  
Постановка ТЗ и наполнение проекта: [Yandex-praktikum](https://github.com/yandex-praktikum).

## Примеры запросов и ответов.
### Добавление нового рецепта.
![Static Badge](https://img.shields.io/badge/POST_запрос-rgb(24,111,175))  
`http://localhost/api/recipes/`
```
{
    "ingredients": [
        {
            "id": 1123,
            "amount": 10
        }
    ],
    "tags": [
        1,
        2
    ],
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
    "name": "string",
    "text": "string",
    "cooking_time": 1
}
```
Ответ JSON:
```
{
    "id": 0,
    "tags": [
        {
            "id": 0,
            "name": "Завтрак",
            "slug": "breakfast"
        } 
    ],
    "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Иванов",
    "is_subscribed": false,
    "avatar": "http://foodgram.example.org/media/users/image.png"
    },
    "ingredients": [
        {
            "id": 0,
            "name": "Картофель отварной",
            "measurement_unit": "г",
            "amount": 1
        }
    ],
    "is_favorited": true,
    "is_in_shopping_cart": true,
    "name": "string",
    "image": "http://foodgram.example.org/media/recipes/images/image.png",
    "text": "string",
    "cooking_time": 1
}
```
### Получение всех тегов.
![Static Badge](https://img.shields.io/badge/GET_запрос-rgb(47,129,50))  
`http://localhost/api/tags/`

Ответ JSON:
```
[
    {
        "id": 0,
        "name": "Завтрак",
        "slug": "breakfast"
    }
]
```
### Частичное обновление рецепта.
![Static Badge](https://img.shields.io/badge/PATCH_запрос-rgb(191,88,29))  
`http://localhost/api/recipes/{id}/`
```
{
    "ingredients": [
        {}
    ],
    "tags": [
        1,
        2
    ],
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
    "name": "string",
    "text": "string",
    "cooking_time": 1
}
```
Ответ JSON:
```
{
    "id": 0,
    "tags": [
        {}
    ],
    "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Иванов",
    "is_subscribed": false,
    "avatar": "http://foodgram.example.org/media/users/image.png"
    },
    "ingredients": [
        {}
    ],
    "is_favorited": true,
    "is_in_shopping_cart": true,
    "name": "string",
    "image": "http://foodgram.example.org/media/recipes/images/image.png",
    "text": "string",
    "cooking_time": 1
}
```
### Удаление подписки
![Static Badge](https://img.shields.io/badge/DEL_запрос-rgb(204,51,51))  
`http://localhost/api/users/{id}/subscribe/`

### Примеры остальных запросов можно посмотреть в [документации](http://localhost/api/docs/).
_Документация будет доступна после запуска [проекта](#instruct)._
#### Инструкция по запуску файла redoc:
Находясь в папке infra, выполните команду docker-compose up. При выполнении этой команды контейнер frontend, описанный в docker-compose.yml, подготовит файлы, необходимые для работы фронтенд-приложения, а затем прекратит свою работу.
По адресу http://localhost изучите фронтенд веб-приложения, а по адресу http://localhost/api/docs/ — спецификацию API.
