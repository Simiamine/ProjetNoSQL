from kafka import KafkaProducer
from faker import Faker
import json
import time
import random

fake = Faker()
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_vehicle_data(vehicle_id):
    return {
        "vehicle_id": vehicle_id,
        "@timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "latitude": float(fake.latitude()),
        "longitude": float(fake.longitude()),
        "speed_kmh": round(random.uniform(0, 120), 2),
        "battery_level": random.randint(10, 100)
    }

if __name__ == "__main__":
    vehicle_ids = [f"veh-{i}" for i in range(1, 6)]

    while True:
        vehicle = random.choice(vehicle_ids)
        data = generate_vehicle_data(vehicle)
        print(f"Sending: {data}")
        producer.send("vehicle-data", data)
        time.sleep(1)