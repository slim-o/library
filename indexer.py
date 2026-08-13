import requests
from urllib.parse import urljoin

base_url = "https://libgen.li/"

api_url = urljoin(base_url, "json.php")

print("API URL:", api_url)
print('')

def api_request(params):
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    #print(response.status_code)
    #print(response.url)
    #print("Data type:", type(response.json()))
    #print("Data keys:", response.json().keys())
    return response.json()

def get_edition(e_id):
    edition_params = {
        "object": "e",
        "ids": e_id
    }
    edition_data = api_request(edition_params)
    return edition_data[e_id] if e_id in edition_data else None

params = {
    "object": "f",
    "id_start": 4604718,
    "id_end": 4604719
}

data = api_request(params)

for file_id, file in data.items():
    #print(file.keys())

    print("File ID:", file_id)
    print("MD5:", file["md5"])
    print("Filesize:", file["filesize"])
    print("Extension:", file["extension"])
    print("Libgen ID:", file["libgen_id"])

    print('')
    print("Editions:")
    editions = file["editions"]

    for edition_id, edition_ref in editions.items():
        print(" - Edition key:", edition_id)
        e_id = edition_ref["e_id"]
        print("   - e_id:", e_id)
        print('')
        edition = get_edition(e_id)
        #print(edition.keys())
        print("   - Edition title:", edition["title"])
        print("   - Edition author:", edition["author"])
        print("   - Edition publisher:", edition["publisher"])
        print("   - Edition year:", edition["year"])
        print("   - Files", edition["files"])
        print('')

