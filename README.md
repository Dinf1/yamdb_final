![workflow](https://github.com/Dinf1/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

- репозиторий сделал публичным
- ссылки на рабочий проект ниже. Но в Yandex.Cloud боевой сервер - прерываемая яндексом виртуальная машина, поэтому можно попасть на момент, когда яндекс остановит ВМ. Постараюсь отследить и поднять заново. Но на всякий случай скрины в папке screens
    - http://158.160.39.229/redoc/
    - http://158.160.39.229/admin/  (admin/admin)
- в yamdb_workflow.yml есть замечание, что не хватает команды docker pull... Не совсем понимаю, зачем она нужна, если на сервере мы размещаем  docker-compose.yaml, в котором основой для контейнера web является образ c Dockerhub, т.е. это и есть аналог docker pull. 

# Проект YaMDb:

Проект YaMDb собирает отзывы пользователей на различные произведения. Развернуть проект можно локально либо на сервере.

Когда Вы запустите проект, по адресу http://server_IP_address/redoc/ будет доступна документация для *YaMDb*. В документации описано, как работает API. Документация представлена в формате *Redoc*.

## Примеры:

Создание публикации методом POST:

Ендпоинт:
```
http://server_IP_address/api/v1/posts/
```

Тело запроса:

```
{
  "text": "текст поста",
  "image": "string",
  "group": 0
}
```

Пример ответа json (код=201):

```
{
  "id": 0,
  "author": "Ваш username",
  "text": "текст поста",
  "pub_date": "2022-01-01T14:15:22Z",
  "image": "string",
  "group": 0
}
```

Частичное обновление комментария методом PATCH:

Ендпоинт, {post_id} - id поста, {id} - id комментария к этому посту':
```
http://server_IP_address/api/v1/posts/{post_id}/comments/{id}/
```

Тело запроса:

```
{
  "text": "текст комментария"
}
```

Пример ответа json (код=201):

```
{
  "id": 0,
  "author": "Ваш username",
  "text": "текст комментария",
  "created": "2022-01-01T14:15:22Z",
  "post": 0
}
```


## Как запустить проект YaMDb на сервере: 

На странице https://github.com/Dinf1/yamdb_final  выполните "форк" - копирование данного репозитория к себе.

Выполните клонирование своего репозитория с сервера GitHub на свой ПК:
``` 
git clone https://github.com/YOUR_USERNAME/api_final_yatube.git
``` 
 
Подготовьте свой сервер, разместите на нем файлы:
- docker-compose.yaml
- nginx/default.conf

Установите на нем:
- docker (https://docs.docker.com/engine/install/)
- docker-compose (https://docs.docker.com/compose/install/)

### В secrets своего репозитория github создайте переменные окружения со следующими параметрами: 
``` 
DB_ENGINE=django.db.backends.postgresql 
DB_NAME=postgres 
POSTGRES_USER=YOUR_USER_FOR_DB 
POSTGRES_PASSWORD=YOUR_PASSWORD_FOR_DB 
DB_HOST=db 
DB_PORT=5432 
SECRET_KEY='YOUR_SECRET_KEY'
DOCKER_PASSWORD=YOUR_PASSWORD_FOR_DOCKERHUB
DOCKER_USERNAME=YOUR_LOGIN_FOR_DOCKERHUB
HOST=IP_YOUR_REAL_SERVER
PASSPHRASE=PASSPHRASE_FOR_CONNECTION_TO_REAL_SERVER
SSH_KEY=PRIVATE_PART_OF_KEY_FOR_CONNECTION_TO_REAL_SERVER
TELEGRAM_TO=YOUR_ID
TELEGRAM_TOKEN=BOT_TOKEN
USER=USER_FOR_CONNECTION_TO_REAL_SERVER
``` 

Далее необходимо выполнить для запуска автотестов, создания образа web и размещение на docker hub, запуска всех контейнеров на сервере, отправки уведомления в Телеграм.
``` 
git add .
git commit -m 'YOUR_COMMENT'
git push
``` 

## Как запустить проект YaMDb локально: 

На странице https://github.com/Dinf1/yamdb_final  выполните "форк" - копирование данного репозитория к себе.

Выполните клонирование своего репозитория с сервера GitHub на свой ПК:
``` 
git clone https://github.com/YOUR_USERNAME/api_final_yatube.git
``` 

Установите на своем ПК:
- docker (https://docs.docker.com/engine/install/)
- docker-compose (https://docs.docker.com/compose/install/)

### В папке проекта infra создайте файл окружения .env со следующими параметрами: 
``` 
DB_ENGINE=django.db.backends.postgresql 
DB_NAME=postgres 
POSTGRES_USER=YOUR_USER_FOR_DB 
POSTGRES_PASSWORD=YOUR_PASSWORD_FOR_DB 
DB_HOST=db 
DB_PORT=5432 
SECRET_KEY='YOUR_SECRET_KEY'
``` 

### Для запуска контейнеров необходимо выполнить из папки infra:
```
sudo docker-compose up -d --build
```
или в зависимости от версии:
```
sudo docker compose up -d --build
```
Далее выполните по очереди команды:
```
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py createsuperuser
sudo docker-compose exec web python manage.py collectstatic --no-input
```
или в зависимости от версии:
```
sudo docker compose exec web python manage.py migrate
sudo docker compose exec web python manage.py createsuperuser
sudo docker compose exec web python manage.py collectstatic --no-input
```
При возникновении ошибки 403 - доступ запрещен, выполнить:
```
sudo chmod u=rwx,g=rwx,o=rwx /var/lib/docker/volumes/infra_static_value/_data
```
### Автор 
Денис Ц. 

