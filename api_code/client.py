import requests
import json

url = "http://localhost:5000/delivery_fee"

payload = {
    "cart_value": 50,
    "delivery_distance": 1000,
    "number_of_items": 5,
    "time": "2023-01-31T15:00:00Z"
}

headers = {
  'Content-Type': 'application/json'
}

response = requests.post(url, data=json.dumps(payload), headers=headers)

if response.status_code == 200:
    delivery_fee = response.json()['delivery_fee']
    print(f"Delivery fee is: {delivery_fee}")
else:
    print(f"Request failed with status code: {response.status_code}")
