from kafka import KafkaConsumer
import json

# Connexion au topic Kafka
consumer = KafkaConsumer(
    "vehicle-data-v2",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id="battery-alert-consumer"
)

print("🛡️ Battery Alert Consumer lancé...")

for message in consumer:
    data = message.value
    battery = data.get("battery_level", 100)
    if battery < 20:
        print(f"⚠️ ALERTE : {data['vehicle_id']} a une batterie faible ({battery}%)")