from kafka import KafkaProducer
import json
import time


producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


events = [
    {"source": "tcp_collector", "message": "connection established", "level": "info"},
    {"source": "udp_collector", "message": "packet received", "level": "info"},
    {"source": "tcp_collector", "message": "timeout error", "level": "error"},
    {"source": "api_server", "message": "POST /telemetry 200", "level": "info"},
    {"source": "api_server", "message": "POST /telemetry 500", "level": "error"},
]


for event in events:
    future = producer.send('telemetry', value=event)
    result = future.get(timeout=10)
    print(f"Отправлено: {event['message']} → partition={result.partition}, offset={result.offset}")
    time.sleep(0.5)


future = producer.send(
    'telemetry',
    key=event['source'].encode('utf-8'),
    value=event
)

    
producer.flush()
producer.close()
print("Producer finish")