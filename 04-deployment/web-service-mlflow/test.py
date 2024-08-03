import requests


ride = { "PULocationID":10, 
"DOLocationID":50,
"duration" :40}

url = 'http://127.0.0.2:9696/predict'

response = requests.post(url , json=ride)


print(response.json())