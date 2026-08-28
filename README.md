Data engineering portfolio


## О проекте
Учебный ELT-ETL пайплайн для практики от сырых данных до агрегатов, с прод airflow


## Статус v0.1 - Airflow + postgres, dbt


## Стек
- Orchestration: Apache airflow 2.10.4 (docker) 
- Database: PostgreSQL 16
- Data source: NYC Taxi(3.3 rows)
- Transformation: dbt


# Архитектура
FileSensor(wait for trigger)
↓
Unstable source check(retry logic demo)
↓
Connection check(count validation)
↓
Get stats by vendor(aggregation)
↓
Log summary (Xcom data passing)


## Что реализовано на v0.1


- Airflow DAG c 5 тасками и зависимостями
- Xcom для передачи данных между тасками
- Retry logic с настраиваемым количеством попыток и задержкой
- on_failure_check для алертинга при финальном провале таске
- FileSensor Для ожидания внешного триггера (poke-based)
- Postgres как аналитическое хранилище, подключение из док-контейнера к хосту


## Что реализовано на v0.3


- dbt: staginng layer (source - stg_trips)
- dbt: marts layer с агрегацией (ref() - vendor_stats)
- dbt tests: unique, not_null - ошибка в колонке словил
- dbt docs: автоматическая документация + lineage graph


## Что реализовано на v0.8

- Airflow + dbt интеграция: DAG вызывает `dbt run` и `dbt test` через BashOperator
- Исправлен реальный баг совместимости Celery/click в образе Airflow (см. ниже)
- HTTP-based alerting: DAG отправляет уведомление о финальном провале таска на внешний webhook
- В проде это был бы Slack/Telegram webhook; из-за сетевых ограничений (блокировка Telegram API) для демонстрации используется webhook.site
- Exponential backoff для retry на нестабильном таске (`retry_exponential_backoff=True`)
- Airflow Variables для хранения секретов (webhook URL) вместо хардкода в коде


## Пример работы (лог из v0.1)


Индексы и партиционирование дали ~5x ускорение запроса:
- Baseline (Seq Scan): 207 ms
- + Index (узкий фильтр): 49 ms  
- + Partitioning by week + Index: 41.8 ms

## Пример работы (v0.3)

![Lineage Graph](docs/images/image-1.png)


## Пример работы (v0.8)

- {
  "text": "🚨 Task Failed\nDAG: taxi_stats_pipeline\nTask: unstable_external_check\nExecution date: 2026-08-27 18:48:14.910677+00:00"
    }


## Разобранные проблемы (реальные баги, не учебные)

- **Celery/click incompatibility**: свежий баг в связке Airflow 2.10.4 + Celery, вызванный обновлением пакета `click` до 8.3.0 — worker падал в вечный restart-loop. Исправлено закреплением версии `click==8.2.1` в Dockerfile (решение подтверждено официальной документацией Astronomer).
- **Docker volume paths**: относительные пути в `docker-compose.yaml` резолвятся относительно расположения самого файла, не текущей директории — источник нескольких ошибок `file not found`.
- **profiles.yml внутри контейнера**: dbt использует разные profiles.yml на хосте и в контейнере — `host.docker.internal` вместо `localhost` для подключения из Docker к сервисам на хосте.


## Roadmap


- dbt
- clickhouse
- spark
- cloud
- scala
- kafka
- data lense
- data lake
- delta lake
- iceberg
(чем больше тем лучше понять)


## Запуск локально

\`\`\`bash
docker-compose up airflow-init
docker-compose up -d
# UI: http://localhost:8080 (airflow/airflow)
\`\`\`