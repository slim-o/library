from urllib.parse import urljoin

from api import base_url, session, headers
from parser import parse_search_results

def search(query):
    
    search_url = urljoin(base_url, "index.php")

    params = {
        "req": query,
        "open": 0,
        "res": 100,
        "view": "simple",
        "phrase": 1,
        "column": "def",
        "covers": "on"
    }


    response = session.get(
        search_url, 
        params=params, 
        headers=headers
    )

    response.raise_for_status()
    #print("Status:", response.status_code)
    #print("URL:", response.url)
    return parse_search_results(response.text)