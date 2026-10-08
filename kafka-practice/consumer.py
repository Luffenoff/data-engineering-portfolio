from kafka import KafkaConsumer
import json


consumer = KafkaConsumer(
    'telemetry',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)


print("Consumer запущен, читаем сообщения...")


for message in consumer:
    event = message.value
    print(f"[partition={message.partition} offset={message.offset}] "
          f"[{event['level'].upper()}] {event['source']}: {event['message']}")
    
    
    
print("consumer Завершён")