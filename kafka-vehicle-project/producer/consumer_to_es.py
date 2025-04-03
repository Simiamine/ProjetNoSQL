from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

# Connexion à Elasticsearch (localhost:9200)
es = Elasticsearch("http://localhost:9200")

# Connexion au topic Kafka
consumer = KafkaConsumer(
    "vehicle-data-v2",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='vehicle-consumer-group'
)

for message in consumer:
    data = message.value
    data["location"] = {
        "lat": data["latitude"],
        "lon": data["longitude"]
    }
    print(f"✅ Message reçu : {data}")
    es.index(index="vehicle-data-v2", document=data)