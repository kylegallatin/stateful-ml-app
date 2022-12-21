import requests
import time
from river import datasets

dataset = datasets.Phishing()

url = "http://0.0.0.0:8080/update_model"

for x, y in dataset:
    time.sleep(0.1)
    data = {"x": x, "y": int(y)}
    print(requests.put(url, json=data).content)