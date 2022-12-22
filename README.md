![workflow](https://github.com/Dinf1/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
 
## Как запустить проект yamdb_final: 
 
Подготовьте свой сервер, разместите на нем файлы:
- docker-compose.yaml
- nginx/default.conf

Установите на нем:
- docker
- docker-compose (https://docs.docker.com/compose/install/)

Далее необходимо выполнить для запуска автотестов, создания образа web и размещение на docker hub, запуска всех контейнеров на сервере, отправки уведомления в Телеграм.
``` 
git add .
git commit -m 'YOUR_COMMENT'
git push
``` 


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

### Автор 
Денис Ц. 

