# m3u-backend
API телеграм бота по просмотру программ показа каналов телевидения.
#
### Как запустить проект:

#### Предварительные требования:
- развернутый PostgreSQL,
- заполненныый .env, см. env.sample

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/abp-ce/m3u_backend.git
```

```
cd m3u_backend
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

```
python3 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
alembic upgrade head
```

Запустить проект:

```
uvicorn main:app --reload
```
### Стек:
 - fastapi 0.89.1
 - SQLAlchemy 1.4.46
 - alembic 1.9.2
 - asyncpg==0.27.0