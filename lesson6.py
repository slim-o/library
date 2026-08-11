import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.request import urlopen

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
}

url = "https://pip.pypa.io/en/stable/search"



params = {
        "q": "install"
    }

def search(query):
    try:
        response = requests.get(url, params=query, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


response = search(params)

print(response.url)
print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")
print(soup.prettify())
print('')
search_results = soup.select("#search-results ul li")

print(f"Found {len(search_results)} results for query '{params['q']}':")
print("--------------------------------------------------")


for result in search_results:
    title = result.select_one("a")
    if title:
        print(f"Title: {title.get_text(strip=True)}")
        print(f"URL: {urljoin(url, title.get('href'))}")
        print("--------------------------------------------------")

#print(response.text)
