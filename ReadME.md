# Currency Statistics API

Асинхронное веб-приложение на **FastAPI** для получения и статистики курсов пяти основных валют (USD, EUR, GBP, JPY, CHF) относительно рубля (RUB). Данные сохраняются в SQLite, предоставляется статистика по запросам.

## 📦 Технологии

- Python 3.10–3.12
- FastAPI
- aiosqlite (асинхронная работа с SQLite)
- httpx (асинхронные HTTP-запросы)
- Pytest + pytest-asyncio + pytest-mock
- GitHub Actions (CI с матрицей версий Python)

## 🚀 Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/yourusername/currency_stats.git
cd currency_stats
```

### 2. Создание виртуального окружения и установка зависимостей

```bash
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

### 3. Запуск приложения

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 4. Проверка работы приложения

Откроите браузер и перейдите по адресу `http://127.0.0.1:8000/docs` для доступа к документации Swagger UI.

## 🔌 API Endpoints

### 1. Получение курсов валют

```bash
GET /rates
```

```json
{
  "usd": 90.12,
  "eur": 98.46,
  "gbp": 115.79,
  "jpy": 0.62,
  "chf": 102.35,
  "timestamp": "2026-04-06T14:30:00.123456"
}
```

### 2. Статистика запросов

```bash
GET /stats
```

```json
{
  "total_requests": 5,
  "average_rates": {
    "usd": 90.08,
    "eur": 98.32,
    "gbp": 115.65,
    "jpy": 0.62,
    "chf": 102.28
  },
  "last_requests": [ ... ]
}
```

## 🧪 Тестирование

```bash
pytest tests/ -v
```

Тесты используют временную базу данных, изолированы друг от друга и мокают внешний API.

## 🔁 GitHub Actions

При каждом пуше или pull request в ветку main запускается CI:
• Проверка на Python 3.10, 3.11, 3.12
• Установка зависимостей
• Запуск тестов
Статус сборки отображается на странице репозитория.

## 📁 Структура проекта

```text
currency_stats/
├── .github/workflows/ci.yml
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── services.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_main.py
├── requirements.txt
├── pytest.ini
└── README.md
```
