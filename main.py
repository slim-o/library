import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

with open("lesson4.html", "r") as file:
    html = file.read()

soup = BeautifulSoup(html, "html.parser")

url = "https://example.com"
url2 = "https://libgen.li/index.php?req=boom"

soup = BeautifulSoup(urlopen(url2), "html.parser")

def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

response = fetch_page(url)
print(response)
#print(html)
books = soup.select(".book")

print(len(books))
for book in books:
    title = book.select_one(".title")
    author = book.select_one(".author")
    year = book.select_one(".year")
    link = book.select_one(".title a")
    format = book.select_one(".format")

    print(f"Title: {title.get_text(strip=True)}")
    print(f"href: { urljoin(url, link.get('href'))}")
    print(f"Author: {author.get_text(strip=True)}")
    print(f"Year: {year.get_text(strip=True)}")
    print(f"Format: {format.get_text(strip=True)}")
    print('')
#print(soup.h1.text)
'''
if response:
    print("Status:", response.status_code)
    print("Headers:", response.headers['Content-Type'])
    print("Body:")
    print(response.text)
#'''