from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

mapping = {
    "mappings": {
        "properties": {
            "@timestamp": {"type": "date"},
            "vehicle_id": {"type": "keyword"},
            "type": {"type": "keyword"},
            "latitude": {"type": "float"},
            "longitude": {"type": "float"},
            "speed_kmh": {"type": "float"},
            "battery_level": {"type": "float"}
        }
    }
}

if not es.indices.exists(index="vehicle-data-v2"):
    es.indices.create(index="vehicle-data-v2", body=mapping)
    print("Index 'vehicle-data-v2' créé avec mapping personnalisé.")
else:
    print("Index 'vehicle-data-v2' existe déjà.")