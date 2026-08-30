# Data Engineering Portfolio

## О проекте

Учебный ELT-пайплайн для практики Data Engineering: от сырых данных до аналитических агрегатов, с полным набором production-паттернов Airflow, dbt и сравнением аналитических СУБД.

## Статус: v1.0 — Airflow + dbt + ClickHouse benchmark

## Стек

- **Orchestration:** Apache Airflow 2.10.4 (Docker)
- **Databases:** PostgreSQL 16, ClickHouse (OLAP benchmark)
- **Data source:** NYC Taxi Trip Data (3.3M rows, Dec 2023)
- **Transformation:** dbt (staging, marts, incremental models)

## Архитектура пайплайна

```
FileSensor (wait for trigger)
    ↓
Unstable Source Check (retry logic demo)
    ↓
Connection Check (count validation)
    ↓
Get Stats by Vendor (aggregation)
    ↓
Log Summary (XCom data passing)
    ↓
dbt run (staging + marts models)
    ↓
dbt test (data quality checks)
```

## Что реализовано

### v0.1 — Airflow foundation

- Airflow DAG с 5 тасками и явными зависимостями
- XCom для передачи данных между тасками
- Retry logic с настраиваемым количеством попыток и задержкой
- `on_failure_callback` для алертинга при финальном провале таска
- FileSensor для ожидания внешнего триггера (poke-based)
- Postgres как аналитическое хранилище, подключение из Docker-контейнера к хосту

### v0.3 — dbt layers

- dbt: staging layer (`source()` → `stg_trips`)
- dbt: marts layer с агрегацией (`ref()` → `vendor_stats`)
- dbt tests: `unique`, `not_null` — тесты поймали реальную опечатку в названии колонки
- dbt docs: автоматическая документация + lineage graph

### v0.8 — Airflow + dbt интеграция

- DAG вызывает `dbt run` и `dbt test` через `BashOperator`
- Исправлен реальный баг совместимости Celery/click в образе Airflow (см. раздел ниже)
- HTTP-based alerting: DAG отправляет уведомление о финальном провале таска на внешний webhook
  (в проде это был бы Slack/Telegram webhook; из-за сетевых ограничений — блокировка Telegram API — для демонстрации используется webhook.site)
- Exponential backoff для retry на нестабильном таске (`retry_exponential_backoff=True`)
- Airflow Variables для хранения секретов вместо хардкода в коде

### v0.9 — dbt incremental models

- Реализована `materialized='incremental'` модель с `is_incremental()` и `unique_key`
- Первый (полный) запуск на 3.3M строк: **11.84s**
- Повторный инкрементальный запуск без новых данных: **0.3s** — данные не пересчитываются заново, обрабатывается только прирост

### v1.0 — ClickHouse benchmark

- ClickHouse развёрнут в Docker (движок `MergeTree`)
- Нативная загрузка parquet напрямую в ClickHouse через табличную функцию `file()`, без Python-прослойки — 3.3M строк за **0.54s**
- Бенчмарк ClickHouse vs Postgres на идентичном агрегирующем запросе
- Проверена консистентность агрегатов между Postgres и ClickHouse после независимой загрузки данных

## Пример работы: SQL-оптимизация (Postgres)

Индексы и партиционирование дали ~5x ускорение запроса:

- Baseline (Seq Scan): 207 ms
- + Index (узкий фильтр): 49 ms
- + Partitioning by week + Index: 41.8 ms

## Пример работы: dbt lineage graph

![Lineage Graph](docs/images/image-1.png)

## Пример работы: HTTP alerting

```json
{
  "text": "🚨 Task Failed\nDAG: taxi_stats_pipeline\nTask: unstable_external_check\nExecution date: 2026-08-27 18:48:14.910677+00:00"
}
```

## ClickHouse vs Postgres — бенчмарк

Запрос: агрегация (avg fare, count) по `vendor_id` с фильтром по дате (узкий диапазон, ~3% от 3.3M строк).

| База | Оптимизация | Время |
|---|---|---|
| Postgres | Seq Scan (без индекса) | 207 ms |
| Postgres | + Index | 49 ms |
| Postgres | + Partitioning + Index | 41.8 ms |
| **ClickHouse** | **Без настройки, "из коробки"** | **~0 ms (округлилось)** |

**Вывод:** разница объясняется архитектурой хранения — ClickHouse колоночный (читает только нужные столбцы: `fare_amount`, `pickup_datetime`, `vendor_id`), Postgres строковый (читает целые строки даже при выборке одной колонки). ClickHouse оптимален для OLAP-агрегаций по широким таблицам; Postgres остаётся предпочтительным для точечных транзакционных операций — у ClickHouse нет полноценных ACID-транзакций и `UPDATE`/`DELETE` в привычном смысле.

## Разобранные проблемы (реальные баги, не учебные)

- **Celery/click incompatibility**: свежий баг в связке Airflow 2.10.4 + Celery, вызванный обновлением пакета `click` до 8.3.0 — worker падал в вечный restart-loop. Исправлено закреплением версии `click==8.2.1` в Dockerfile (решение подтверждено официальной документацией Astronomer).
- **Docker volume paths**: относительные пути в `docker-compose.yaml` резолвятся относительно расположения самого файла, а не текущей рабочей директории — источник нескольких ошибок `file not found`.
- **profiles.yml внутри контейнера**: dbt использует разные `profiles.yml` на хосте и в контейнере — `host.docker.internal` вместо `localhost` для подключения из Docker к сервисам на хосте.
- **Jinja-комментарии внутри `{{ config() }}`**: обычный SQL-комментарий `--` внутри блока `{{ }}` ломает парсинг Jinja-выражения — для комментариев внутри `{{ }}` нужен `{# ... #}`.

## Roadmap

**Done:**
- ✅ dbt (staging, marts, tests, docs, incremental)
- ✅ ClickHouse (setup, native load, OLAP benchmark)

**Next:**
- Spark (batch-обработка)
- Asyncio / сокеты (backend-направление)

**Later (продвинутый уровень):**
- Kafka, Cloud (AWS / Yandex Cloud)
- Data Lakehouse: Iceberg, Delta Lake, Trino
- Scala

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