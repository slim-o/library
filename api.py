import requests
from urllib.parse import urljoin


base_url = "https://libgen.li/"
api_url = urljoin(base_url, "json.php")
page_extension = "ads.php?md5="

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0"
}

def api_request(params):
    response = session.get(
        api_url, 
        params=params, 
        headers=headers
    )
    
    #print("Status:", response.status_code)
    #print("URL:", response.url)
    #print("Content-Type:", response.headers.get("Content-Type"))
    #print("Response:", response.text[:500])
    #print("Data type:", type(response.json()))
    #print("Data keys:", response.json().keys())
    
    response.raise_for_status()
    return response.json()

def get_edition(e_id):
    edition_params = {
        "object": "e",
        "ids": e_id
        #"isbn": 9781408803721
    }
    edition_data = api_request(edition_params)
    return edition_data[e_id] if e_id in edition_data else None

def find_editions(isbn):
    edition_params = {
        "object": "e",
        "isbn": isbn
    }
    editions = api_request(edition_params)
    return editions

def get_files(id_start, id_end):
    file_params = {
        "object": "f",
        "id_start": id_start,
        "id_end": id_end
    }
    file_data = api_request(file_params)
    return file_data

def get_file(file_id):
    file_params = {
        "object": "f",
        "ids": file_id
    }
    file_data = api_request(file_params)
    return file_data
