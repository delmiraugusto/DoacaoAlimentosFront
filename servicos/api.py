import requests

BASE_URL = "http://192.168.1.3:8080/doacoes/"

def get(endpoint):
    resp = requests.get(f"{BASE_URL}{endpoint}")
    resp.raise_for_status()
    return resp.json()

def get_por_id(endpoint, id_):
    resp = requests.get(f"{BASE_URL}{endpoint}/{id_}")
    resp.raise_for_status()
    return resp.json()

def post(endpoint, dados):
    resp = requests.post(f"{BASE_URL}{endpoint}", json=dados)
    resp.raise_for_status()
    return resp.json()

def put(endpoint, id_, dados):
    resp = requests.put(f"{BASE_URL}{endpoint}/{id_}", json=dados)
    resp.raise_for_status()
    return resp.json()

def delete(endpoint, id_):
    resp = requests.delete(f"{BASE_URL}{endpoint}/{id_}")
    resp.raise_for_status()
    return {"message": "Excluído com sucesso"}
