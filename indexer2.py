import requests
from urllib.parse import urljoin

base_url = "https://libgen.li/"

api_url = urljoin(base_url, "json.php")

print("API URL:", api_url)

params = {
    "object": "e",
    "ids": 3115609
}

response = requests.get(api_url, params=params)

print(response.status_code)
print(response.url)

data = response.json()
#print("Data type:", type(data))
print(data)