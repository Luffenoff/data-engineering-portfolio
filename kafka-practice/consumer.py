from kafka import KafkaConsumer
import json


consumer = KafkaConsumer(
    'telemetry',
    bootstrap_servers='localhost:9092',
    group_id='telemetry-processors',
    auto_offset_reset='earliest',
    consumer_timeout_ms=5000,
)

consumer.subscribe(['Telemetry'])
print("Consumer запущен, читаем сообщения...")


for message in consumer:
    event = json.loads(message.value.decode('utf-8'))
    print(f"[partition={message.partition} offset={message.offset}] "
          f"[{event['level'].upper()}] {event['source']}: {event['message']}")
    

    
print("consumer Завершён")
consumer.close()