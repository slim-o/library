import requests

response = requests.get("https://libgen.im/search.php?req=python")

print(response)