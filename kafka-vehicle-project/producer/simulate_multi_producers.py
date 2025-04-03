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

# Dictionnaire de véhicules par type
vehicles = {
    "car": [f"veh-{i}" for i in range(1, 4)],
    "truck": [f"truck-{i}" for i in range(1, 3)],
    "scooter": [f"scooter-{i}" for i in range(1, 3)],
}

def generate_data(vehicle_id, vehicle_type):
    return {
        "vehicle_id": vehicle_id,
        "type": vehicle_type,
        "@timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "latitude": float(fake.latitude()),
        "longitude": float(fake.longitude()),
        "speed_kmh": round(random.uniform(10, 120), 2),
        "battery_level": random.randint(10, 100)
    }

if __name__ == "__main__":
    all_vehicles = [(v_type, v_id) for v_type, ids in vehicles.items() for v_id in ids]

    while True:
        v_type, v_id = random.choice(all_vehicles)
        data = generate_data(v_id, v_type)
        print(f"Sending: {data}")
        producer.send("vehicle-data", data)
        time.sleep(1)