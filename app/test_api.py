import requests
import json

url = "http://localhost:8000/buscar"
payload = {"query": "fone", "cep": "12345678"}
headers = {"Content-Type": "application/json"}

try:
    print(f"Testando POST {url}...")
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"Status: {response.statusCode}")
    print(f"Resposta: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Erro ao testar: {e}")
