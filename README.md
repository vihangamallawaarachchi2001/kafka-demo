# Real-Time Event Processing with Kafka and Redis

A local development stack for building event-driven applications using:
- **Apache Kafka** (KRaft mode — no ZooKeeper!)
- **Redis** (with AOF persistence for real-time state)

Perfect for prototyping streaming analytics, clickstream processing, or real-time dashboards.

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose installed
- Python 3.8+ (for producer/processor scripts)

### 1. Clone the repository
```bash
git clone https://github.com/your-username/kafka-redis-demo.git
cd kafka-redis-demo

2. Start Kafka and Redis
bash


1
docker compose up -d



This will launch:

    Kafka on localhost:9092 (KRaft mode, no ZooKeeper)
    Redis on localhost:6379 (with AOF persistence enabled)


3. Run the event processor

In a new terminal, activate your virtual environment and run:
bash


1
python3 processor.py



This script:

    Consumes events from the demo Kafka topic
    Maintains a 60-second sliding window per event_type
    Stores real-time averages in Redis under keys like avg:click


4. Send test events

In another terminal:
bash


1
python3 producer.py



This generates mock user events (page_view, click, purchase) and sends them to Kafka.
5. Query real-time metrics

Use the included FastAPI service:
bash


1
uvicorn api:app --reload



Then visit:

    http://localhost:8000  → health check
    http://localhost:8000/average?event_type=click  → get real-time average


💾 Persistence

Data survives container restarts thanks to Docker volumes:

    Kafka logs → kafka_kraft volume
    Redis data → redis_data volume (AOF enabled)


To reset data:
bash


1
docker compose down -v


📁 Project Structure
.
├── docker-compose.yaml    # Kafka + Redis services
├── redis.conf             # Redis config (AOF enabled)
├── producer.py            # Generates mock events to Kafka
├── processor.py           # Aggregates & stores in Redis
├── api.py                 # FastAPI endpoint to read metrics
└── README.md


🛠️ Customization

    Change window size: edit WINDOW = timedelta(seconds=60) in processor.py
    Add new event types: modify generate_event() in producer.py
    Adjust Kafka/Redis configs: edit docker-compose.yaml or redis.conf


📜 License

MIT 
