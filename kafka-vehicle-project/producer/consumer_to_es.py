from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

# Connexion à Elasticsearch (localhost:9200)
es = Elasticsearch("http://localhost:9200")

# Connexion au topic Kafka
consumer = KafkaConsumer(
    "vehicle-data",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='vehicle-consumer-group'
)

for message in consumer:
    data = message.value
    print(f"Received: {data}")

    # Indexation dans Elasticsearch
    es.index(index="vehicle-data", document=data)