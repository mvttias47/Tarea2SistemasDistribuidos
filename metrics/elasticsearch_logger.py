import requests
import json

def log_to_elasticsearch(data):
    url = 'http://localhost:9200/metrics/_doc'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"Métricas enviadas a Elasticsearch con estado: {response.status_code}")
