import requests


json = { "PULocationID":10, 
"DOLocationID":50,
"duration" :40}

url = ' http://127.2.0.1:9696/predict'

response = requests.post(url , json)


print(response.json())