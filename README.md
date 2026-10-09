# Wallet API

REST API для работы с кошельками. FastAPI, SQLAlchemy (async), PostgreSQL, Alembic.

## Запуск

```bash
docker compose up --build
```

Приложение: http://127.0.0.1:8000, документация: http://127.0.0.1:8000/docs.
Миграции применяются автоматически при старте.

## API

- `POST /api/v1/wallets` — создать кошелёк
- `GET /api/v1/wallets/{wallet_id}` — получить баланс
- `POST /api/v1/wallets/{wallet_id}/operation` — пополнить или списать

```json
{"operation_type": "DEPOSIT", "amount": 1000}
```

`operation_type`: `DEPOSIT` или `WITHDRAW`. 

Ошибки: 

- `404` — кошелёк не найден
- `409` — недостаточно средств 
- `422` — невалидный запрос

## Тесты

```bash
docker compose run --rm tests
```