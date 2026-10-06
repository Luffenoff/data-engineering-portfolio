from kafka import KafkaConsumer
import json


consumer = KafkaConsumer(
    'telemetry',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)