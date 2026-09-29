# Networking Practice

TCP/UDP сокеты, asyncio, FastAPI — от низкоуровневых сокетов до HTTP API.  
Всё запускалось локально на Windows, баги реальные.

## Структура

networking-practice/
├── udp/ # UDP датаграммы: sync и asyncio.DatagramProtocol
├── tcp/ # TCP стримы: sync и asyncio.start_server
├── fastapi/ # HTTP API поверх asyncio: telemetry collector
└── concurrency/ # GIL демо: threading vs multiprocessing vs asyncio



## Ключевые результаты

### UDP/TCP: sync vs asyncio
| Версия | Поведение |
|---|---|
| Sync сервер | `accept()`/`recvfrom()` блокирует поток — один клиент за раз |
| Asyncio сервер | event loop — несколько клиентов конкурентно в одном потоке |

**Доказательство:** два клиента с задержкой 3s:
- sync: ~6s (последовательно)
- asyncio: ~3s (конкурентно)

### GIL: threading vs multiprocessing
CPU-bound задача (вычисления):
| Подход | Время | Причина |
|---|---|---|
| Threading (4 потока) | 4.07s | GIL не даёт параллелизма для CPU-bound |
| Multiprocessing (4 процесса) | 2.44s | Реальный параллелизм (~1.8x) |

### FastAPI telemetry collector
- `POST /telemetry` — приём событий с Pydantic валидацией
- `GET /events` — просмотр накопленных событий
- `GET /health` — статус сервера

## Запуск

**TCP сервер + клиент:**
```bash
# Терминал 1
python tcp/tcp_server_async.py

# Терминал 2  
python tcp/tcp_client_test.py
```

**FastAPI:**
```bash
cd fastapi
uvicorn fastapi_server:app --host 127.0.0.1 --port 8001 --reload
```

## Разобранные баги
- `WinError 10013` — порт занят, решение: сменить порт
- Pydantic v1/v2 конфликт — `pip install --upgrade pydantic fastapi`
- Пакеты в системный Python вместо venv — всегда активировать venv перед pip install
- Windows multiprocessing spawn trap — обязательный `if __name__ == "__main__"`