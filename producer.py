import json
import time
import random
import datetime
from confluent_kafka import Producer

producer_config = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(producer_config)

def delivery_report(err, msg):
    if err:
        print(f"Delivery report error: {err}")
    else:
        print(f'✅ Sent to {msg.topic()} [partition {msg.partition()}] at offset {msg.offset()}')

def generate_event():
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "user_id": f"user_{random.randint(1,10)}",
        "event_type": random.choice(["page_view", "click", "purchase"]),
        "value": round(random.uniform(1.0, 100.0), 2)
    }

try:
    while True:
        event = generate_event()
        producer.produce(
            topic='demo',
            value=json.dumps(event).encode('utf-8'),  # ✅ fixed here
            callback=delivery_report
        )
        producer.poll(0)
        print(f"Produced: {event}")
        time.sleep(3)
except KeyboardInterrupt:
    print("\nFlushing and exiting...")
finally:
    producer.flush()