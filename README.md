# Сервис сбора баллов ЕГЭ (FastAPI + Telegram Bot)

Прототип сервиса, который позволяет ученикам регистрироваться и вводить баллы ЕГЭ через Telegram-бота.  
Бизнес-логика реализована через FastAPI, база данных — PostgreSQL.  

---

# Требования

- Docker Desktop
- Python 3.11+ (для локальной разработки)
- IDE for Python (e.g. PyCharm or Visual Code, я делала в PyCharm)

# Настройка

1. Копируем GitHub проект
   git clone https://github.com/ТВОЙ_ЮЗЕРНЕЙМ/НАЗВАНИЕ_РЕПО.git (индивидуально для вашего IDE)

2. Создаем .env файл
   Прописываем туда токен вашего бота, ссылку на ваш FastAPI и на базу данных.
  BOT_TOKEN=ваш_токен_бота
  DATABASE_URL=postgresql+psycopg2://user:password@db:port/umschoolkz
  API_URL=http://api:8000   

# Запуск через Docker

 1. Поднять все сервисы:
    docker-compose up --build

# Проверка работы
FastAPI: http://localhost:8000/docs — Swagger UI для проверки эндпоинтов.

Telegram Bot: написать команду:

/start, далее выйдет меню.

