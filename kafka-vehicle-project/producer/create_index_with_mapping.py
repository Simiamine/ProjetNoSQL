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
            "location": {"type": "geo_point"},  # <-- Ajout ici
            "speed_kmh": {"type": "float"},
            "battery_level": {"type": "float"}
        }
    }
}

# Supprimer l'index existant
if es.indices.exists(index="vehicle-data-v2"):
    es.indices.delete(index="vehicle-data-v2")

# Créer l'index
es.indices.create(index="vehicle-data-v2", body=mapping)
print("Index 'vehicle-data-v2' avec geo_point créé.")