# Foodgram
![example workflow](https://github.com/Unpatches/foodgram-project-react/actions/workflows/main.yml/badge.svg)

# Описание
    
Учебный проект студента Яндекс.Практикум. Веб сервис дает возможность делиться своими рецептами, искать рецепты других. При необходимости пользователь может подписаться на интересующего его автора, добавлять рецепты в избранное, а также скачивать список ингредиентов перед походом в магазин.



Развернутый проект находиться по адресу http://51.250.9.230/



# Запуск на локальном сервере

1. Клонировать репозиторий

```bash
git clone https://github.com/Unpatches/foodgram-project-react.git
```

2. Установить docker и docker-compose

Инструкция по установке доступна в официальной инструкции

3. В папке с проектом перейти в infra и создать файл .env

Добавить следующее содержимое
```
SECRET_KEY = Секретный ключ django
ALLOWED_HOSTS = Разрешенные подключения
DB_ENGINE= django.db.backends.postgresql
DB_NAME= Имя базы данных
POSTGRES_USER= Пользователь базы данных
POSTGRES_PASSWORD= Пароль базы данных
DB_HOST= Хост базы данных
DB_PORT= Порт базы данных
```
4. В папке infra выполнить команду
```
docker-compose up
```

## Запуск на удаленном сервере
1. В папке с проектом перейти в infra и создать файл .env 
с таким же содержимым как и для запуска на локальном сервере
2. Копировать файлы из папки infra на сервер
```
scp docker-compose.yaml <user>@<server-ip>:
scp .env <user>@<server-ip>:
scp nginx.conf <user>@<server-ip>:
```

3. Cоздать переменные окружения в разделе `secrets` гитхаб репозитория:
```
DOCKER_PASSWORD # Пароль от Docker Hub
DOCKER_USER # Логин от Docker Hub
HOST # Публичный ip адрес сервера
USER # Пользователь зарегистрированный на сервере
PASSPHRASE # Если ssh-ключ защищен фразой-паролем
SSH_KEY # Приватный ssh-ключ
TG_CHAT_ID # ID телеграм-аккаунта
TELEGRAM_TOKEN # Токен бота
```
4. В nginx.conf указать server_name(ip or domain)