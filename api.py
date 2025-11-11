from fastapi import FastAPI
import redis

app = FastAPI()
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.get("/average")
def get_average(event_type: str):
  value = r.get(f"avg:{event_type}")
  if not value:
    return {"event_type": event_type, "average": None, "status": "No data yet"}
  return {"event_type": event_type, "average": float(value)}

@app.get('/')
def root():
  return {"status": "Real-Time Analytics API is running 🚀"}