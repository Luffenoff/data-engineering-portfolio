### Python collector, sendto, stress, api



### Syslog-collector

## цепочка UDP → asyncio Queue → batch insert в SQLite → FastAPI (/logs, /stats)
## стресс-тест: 2000 пакетов за один прогон, потерь нет (на localhost)
## баги, которые разобрал: дублирующий DB_PATH, относительные пути, UDP не сообщает об отсутствии слушателя, WinError 10055


### Kafka


##  Kafka (producer/consumer, партиции, ключи, consumer group, LAG)


## Clickhouse