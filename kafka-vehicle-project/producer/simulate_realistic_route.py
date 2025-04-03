from kafka import KafkaProducer
import json
from datetime import datetime, timedelta
import time
import numpy as np
from geopy.distance import geodesic

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Définir les véhicules et leurs parcours
vehicles = {
    "veh-42": {
        "type": "car",
        "route": [
            (48.8566, 2.3522),
            (48.8605, 2.3364),
            (48.8655, 2.3212),
            (48.8738, 2.2950),
            (48.8584, 2.2945),
            (48.8500, 2.2780),
            (48.8373, 2.2876),
            (48.8401, 2.3256),
            (48.8506, 2.3469),
            (48.8566, 2.3522)
        ]
    },
    "bus-7": {
        "type": "bus",
        "route": [
            (45.7578, 4.8320),  # Lyon Centre
            (45.7600, 4.8500),
            (45.7650, 4.8700),
            (45.7700, 4.8800),
            (45.7750, 4.8900),
            (45.7777, 4.8350)   # Retour
        ]
    },
    "truck-21": {
        "type": "truck",
        "route": [
            (43.2965, 5.3698),  # Marseille
            (43.2990, 5.3800),
            (43.3050, 5.3900),
            (43.3100, 5.4000),
            (43.3200, 5.4100),
            (43.2965, 5.3698)   # Retour
        ]
    }
}

# Initialiser les états
vehicle_states = {}

for vid, config in vehicles.items():
    vehicle_states[vid] = {
        "route_index": 0,
        "step": 0,
        "speed": np.random.uniform(8, 15),
        "battery": 100,
        "pause_counter": 0,
        "time": datetime.utcnow()
    }

# Simulation continue
while True:
    for vid, config in vehicles.items():
        state = vehicle_states[vid]
        route = config["route"]
        idx = state["route_index"]
        if idx >= len(route) - 1:
            state["route_index"] = 0
            state["step"] = 0
            idx = 0

        lat_start, lon_start = route[idx]
        lat_end, lon_end = route[idx + 1]

        segment_distance = geodesic((lat_start, lon_start), (lat_end, lon_end)).km
        step_distance = 0.02
        steps = int(segment_distance / step_distance)

        # Avancement dans le tronçon
        j = state["step"]
        fraction = j / steps
        lat = lat_start + fraction * (lat_end - lat_start)
        lon = lon_start + fraction * (lon_end - lon_start)

        # Pause / accélération
        if state["pause_counter"] > 0:
            speed = 0
            state["pause_counter"] -= 1
        else:
            speed_var = np.random.uniform(-1, 1)
            state["speed"] = max(2, min(18, state["speed"] + speed_var))
            if np.random.rand() < 0.01:
                state["pause_counter"] = np.random.randint(30, 90)

        # Batterie
        state["battery"] = max(0, state["battery"] - 0.02)

        # Timestamp
        now = state["time"]

        message = {
            "vehicle_id": vid,
            "type": config["type"],
            "@timestamp": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "speed_kmh": round(state["speed"], 2),
            "battery_level": round(state["battery"], 1)
        }

        print("Sending:", message)
        producer.send("vehicle-data-v2", key=vid.encode(), value=message)

        # Avancer la simulation
        state["time"] += timedelta(seconds=1)
        state["step"] += 1
        if state["step"] >= steps:
            state["route_index"] += 1
            state["step"] = 0

    time.sleep(1)