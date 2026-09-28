# Data Engineering Portfolio

Учебный DE-пайплайн: от сырых данных до аналитических агрегатов.  
Весь стек запускался локально, все проблемы реальные — не туториал.

## Статус: v1.6 — TCP/UDP collectors + FastAPI

## Стек

| Слой | Технологии |
|---|---|
| Orchestration | Apache Airflow 2.10.4 (Docker) |
| Databases | PostgreSQL 16, ClickHouse (OLAP) |
| Transformation | dbt (staging, marts, incremental) |
| Batch processing | Apache Spark / PySpark 4.2.0 |
| Networking | TCP/UDP сокеты (sync + asyncio) |
| API | FastAPI + Pydantic + uvicorn |
| Data source | NYC Taxi Trip Data, Dec 2023 (3.3M rows) |

## Что реализовано

### v0.1 — Airflow foundation
- DAG с 5 тасками и явными зависимостями
- XCom для передачи данных между тасками
- Retry logic с exponential backoff
- `on_failure_callback` → HTTP alerting на webhook
- FileSensor для ожидания внешнего триггера

### v0.3 — dbt layers
- staging layer: `source()` → `stg_trips`
- marts layer: `ref()` → `vendor_stats`
- dbt tests поймали реальную опечатку в названии колонки
- dbt docs + lineage graph

### v0.8 — Airflow + dbt интеграция
- `dbt run` и `dbt test` через `BashOperator` внутри DAG
- Исправлен реальный баг: Celery/click 8.3.0 несовместимость → pin на 8.2.1
- HTTP alerting через webhook.site (Telegram заблокирован в сети — задокументировано)
- Airflow Variables для хранения конфигов

### v0.9 — dbt incremental models
- `materialized='incremental'` с `is_incremental()` и `unique_key`
- Полный прогон 3.3M строк: **11.84s**
- Инкрементальный перезапуск без новых данных: **0.3s**

### v1.0 — ClickHouse OLAP benchmark
- ClickHouse в Docker, движок MergeTree
- Нативная загрузка parquet через `file()`: 3.3M строк за **0.54s**
- Бенчмарк на идентичном агрегирующем запросе vs Postgres

| База | Оптимизация | Время |
|---|---|---|
| Postgres | Seq Scan | 207 ms |
| Postgres | + Index | 49 ms |
| Postgres | + Partitioning + Index | **41.8 ms** |
| ClickHouse | Без настройки | **~0 ms** |

Разница: ClickHouse колоночный — читает только нужные столбцы.  
Postgres строковый — читает целые строки. ClickHouse выигрывает на OLAP-агрегациях,  
Postgres предпочтительнее для точечных транзакций (полноценный ACID, UPDATE/DELETE).

### v1.1–v1.3 — Apache Spark
- PySpark 4.2.0, local[*] mode
- DataFrame API и Spark SQL — идентичные результаты
- Разобран physical plan: column pruning, shuffle/Exchange, partial aggregation
- Кросс-проверка агрегатов: Postgres = ClickHouse = Spark ✅

### v1.4 — Asyncio & UDP/TCP networking
- sync vs async демо: 6s → 2s на трёх параллельных I/O-bound задачах
- UDP-сервер: sync и `asyncio.DatagramProtocol` версии
- TCP-сервер: sync (`socket.SOCK_STREAM`) и `asyncio.start_server` версии
- Доказана конкурентность asyncio: два клиента с задержкой 3s обслуживаются за ~3s,  
  а не за 6s как в sync-версии — один поток, event loop

### v1.6 — FastAPI telemetry collector
- REST API поверх asyncio: `POST /telemetry`, `GET /events`, `GET /health`
- Pydantic v2 валидация входящего JSON
- In-memory хранилище событий с счётчиком
- Разобраны реальные баги: конфликт Pydantic v1/v2, порт занят (WinError 10013),
  пакеты установились в системный Python вместо venv

## Разобранные баги (реальные, не учебные)

| Баг | Причина | Решение |
|---|---|---|
| Airflow worker restart loop | click 8.3.0 несовместим с Celery | pin `click==8.2.1` |
| dbt не видит Postgres | `localhost` в контейнере ≠ хост | `host.docker.internal` |
| Jinja парсинг падает | `--` комментарий внутри `{{ }}` | использовать `{# #}` |
| FastAPI ImportError | Pydantic v1 в venv, v2 ожидается | `pip install --upgrade pydantic fastapi` |
| uvicorn WinError 10013 | порт 8000 занят системным процессом | сменить порт на 8001 |

## Запуск локально

**Airflow + dbt:**
```bash
cd airflow-practice
docker-compose up airflow-init
docker-compose up -d
# UI: http://localhost:8080 (airflow/airflow)
```

**ClickHouse:**
```bash
cd clickhouse-practice
docker-compose up -d
```

**FastAPI коллектор:**
```bash
cd scripts
uvicorn fastapi_server:app --host 127.0.0.1 --port 8001 --reload
```

## Roadmap
- [ ] Kafka (producer/consumer, топики)
- [ ] Cloud: AWS S3 + Glue или Yandex Cloud
- [ ] Data Lakehouse: Delta Lake / Iceberg
- [ ] Scala (основы для Spark)