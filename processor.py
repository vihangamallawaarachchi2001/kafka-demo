import json, time
from datetime import datetime, timedelta
from collections import defaultdict, deque
from confluent_kafka import Consumer
import redis

consumer_config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "order-tracker",
    "auto.offset.reset": "earliest"
}

consumer = Consumer(consumer_config)
consumer.subscribe(["demo"])

WINDOW = timedelta(seconds=60)
data_window = defaultdict(deque)
latest_event_time = datetime.min  # tracks the newest event time seen

print("Real-time Processor Started...")


try:
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Consumer error:", msg.error())
            continue

        event = json.loads(msg.value().decode('utf-8'))
        event_type = event['event_type']
        timestamp = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00').rstrip('Z'))
        value = event['value']

        # Update latest event time
        if timestamp > latest_event_time:
            latest_event_time = timestamp

        # Add new event
        data_window[event_type].append((timestamp, value))

        # Evict events older than (latest_event_time - WINDOW)
        cutoff = latest_event_time - WINDOW
        while data_window[event_type] and data_window[event_type][0][0] < cutoff:
            data_window[event_type].popleft()

        # Compute stats
        values = [v for _, v in data_window[event_type]]
        if values:
            avg = sum(values) / len(values)
            print(f"📊 {event_type:<10} → count={len(values):<3} avg={avg:.2f}")
            r.set(f"avg:{event_type}", avg)
        else:
            print(f"📊 {event_type:<10} → no data in window")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nShutting down consumer...")
finally:
    consumer.close()