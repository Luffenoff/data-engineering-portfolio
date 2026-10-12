from kafka import KafkaConsumer
import json


consumer = KafkaConsumer(
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    consumer_timeout_ms=5000,
)


consumer.subscribe(['telemetry'])
print("Subscribed, polling...")


for msg in consumer:
    print(F"Got: {msg.value}")
    break


consumer.close()
print("Done")