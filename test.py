import requests

response = requests.post("https://tomsoderlund-rest-api-with-gradio.hf.space/run/predict", json={
  "data": [
    "hello world",
]}).json()

data = response["data"]
print(data)