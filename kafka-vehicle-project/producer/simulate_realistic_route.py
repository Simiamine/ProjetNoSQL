from kafka import KafkaProducer
import json
from datetime import datetime, timedelta
import time
import numpy as np
from geopy.distance import geodesic

# Kafka setup
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

vehicle_id = "veh-42"
vehicle_type = "car"

# Itinéraire simulé
route_points = [
    (48.8566, 2.3522),  # Paris
    (48.8605, 2.3364),
    (48.8655, 2.3212),
    (48.8738, 2.2950),
    (48.8584, 2.2945),  # Tour Eiffel
    (48.8500, 2.2780),
    (48.8373, 2.2876),
    (48.8401, 2.3256),
    (48.8506, 2.3469),
    (48.8566, 2.3522)   # Retour
]

start_time = datetime.utcnow()
current_time = start_time
speed = np.random.uniform(10, 15)
battery = 100
pause_counter = 0

for i in range(len(route_points) - 1):
    lat_start, lon_start = route_points[i]
    lat_end, lon_end = route_points[i + 1]

    segment_distance = geodesic((lat_start, lon_start), (lat_end, lon_end)).km
    step_distance = 0.02  # ≈20 mètres
    steps = int(segment_distance / step_distance)

    for j in range(steps):
        fraction = j / steps
        lat = lat_start + fraction * (lat_end - lat_start)
        lon = lon_start + fraction * (lon_end - lon_start)

        if pause_counter > 0:
            speed = 0
            pause_counter -= 1
        else:
            speed_variation = np.random.uniform(-1, 1)
            speed = max(2, min(18, speed + speed_variation))
            if np.random.rand() < 0.02:
                pause_counter = np.random.randint(30, 90)

        battery = max(0, battery - 0.01)

        message = {
            "vehicle_id": vehicle_id,
            "type": vehicle_type,
            "@timestamp": current_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "speed_kmh": round(speed, 2),
            "battery_level": round(battery, 1)
        }

        print("Sending:", message)
        producer.send("vehicle-data-v2", value=message)
        time.sleep(1)
        current_time += timedelta(seconds=1)