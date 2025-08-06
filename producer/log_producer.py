import random
import time
import json
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

product_ids = [f"product_{i}" for i in range(1, 21)]
user_ids = [f"user_{i}" for i in range(1, 101)]

def generate_log(event_type):
    log = {
        "userId": random.choice(user_ids),
        "productId": random.choice(product_ids),
        "timestamp": datetime.now().isoformat()
    }
    if event_type == "purchase":
        log["price"] = round(random.uniform(10, 100), 2)
    return log

event_types = ["click", "expose", "purchase"]

while True:
    event = random.choice(event_types)
    log = generate_log(event)
    topic = f"{event}-log"
    producer.send(topic, value=log)
    print(f"[{topic}] Sent: {log}")
    time.sleep(random.uniform(0.3, 1.5))
