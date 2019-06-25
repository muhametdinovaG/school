## Развертка рабочего проекта
Для разработки создаем виртуальное окружение с python3:

`virtualenv -p python3 utv_school`

После этого активируем его соответсвенно командой:

`source /path/to/utv_school/bin/activate`

Переходим в папку с проектом:

`cd /path/to/utv_school`

и запускаем установку зависимостей:

`pip install -r requirements/requirements.txt`

После установки зависмиостей идем в каталог проекта **configs/settings** и создаем файл **local.py**

Пример содержания есть в файле **local.py.example**

После всех манипуляций необходимо применить миграции:

`python manage.py migrate`

## local.py
Этот файл занесен в **.gitignore** и предназначен для указания специфических локальных настроек.

Для разработки файл local.py должен начинаться с импорта:

`from .dev import *`

Для развертки в production-окружении соответсвенно:

`from .production import *`

Параметр SECRET_KEY вынесен из бызовых настроек и его также нужно указать в **local.py** 

Так же там необходимо указать параметры соединения с БД - **DATABASES**

Так же в production-окружении в этот файл желательно писать доступы к каким-то внешним сервисам, которые всем подряд знать необязательно.

Ну и в принципе в нем можно переопределить любые базовые настройки


## Работа с актуальными данными.
- Обновить статику скриптом './get_media.sh'
- Загрузить актуальную базу (postgres 9.6) `./get_dump.sh`. Дамп базы снимается на сервере раз в сутки, иначе на сервере `./get_dump.sh`.

Создание базы и пользователя в postgres:

```bash
sudo -u postgres psql
```

```SQL
# создание пользователя
CREATE USER utv_school WITH PASSWORD 'school_pass';
# создание базы
CREATE DATABASE utv_school
  WITH OWNER = utv_school
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'ru_RU.UTF-8'
       LC_CTYPE = 'ru_RU.UTF-8'
       CONNECTION LIMIT = -1;
# права на базу
GRANT CONNECT, TEMPORARY ON DATABASE utv_school TO public;
GRANT ALL ON DATABASE utv_school TO postgres;
GRANT ALL ON DATABASE utv_school TO utv_school;
```

## Работа с webpack
При разработке запускаем в терминале:

`npm run dev`

При деплое необходимо на сервере из папки utv_school запустить:

`npm run build`

Только после этого запускаем файл update.sh