import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

base_url = "https://libgen.li/"

api_url = urljoin(base_url, "json.php")

print("API URL:", api_url)
print('')

### BEUTIFUL SOUP

session = requests.Session()
headers = {"User-Agent": "Mozilla/5.0"}
download_page = ''
page_extension = "ads.php?md5="

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

def parse_search_results(html):
    soup = BeautifulSoup(html, "html.parser")

    rows = soup.select("#tablelibgen tbody tr")

    results = []
    seen = set()

    for row in rows:
        link = row.select_one("a[href]")

        if not link:
            continue

        edition_id = link["href"].split("=")[-1]

        if edition_id in seen:
            continue

        seen.add(edition_id)

        image = row.select_one("img[src]")
        image_url = image["src"] if image else None

        title_element = row.select_one("td:nth-of-type(2) a")
        title = title_element.get_text(strip=True) if title_element else None

        author_element = row.select_one("td:nth-of-type(3)")
        author = author_element.get_text(strip=True) if author_element else None

        results.append({
            "edition_id": edition_id,
            "image_url": image_url,
            "title": title,
            "author": author
        })

    return results

def get_download_link(md5):

    download_page = urljoin(base_url, page_extension + md5)
    response = session.get(download_page, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")


    for link in soup.find_all("a", href=True):
        if link["href"].startswith("get.php?"):
            #print(link["href"])
            return urljoin(base_url, link["href"])


### API REQUEST FUNCTIONS


def api_request(params):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(api_url, params=params, headers=headers)
    
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

### PROGRAM LOGIC

def get_search_results(query):

    results = search(query)

    enriched_results = []

    for result in results:

        edition_id = result["edition_id"]

        edition = get_edition(edition_id)

        if edition is None:
            continue

        enriched_result = {
            "edition_id": edition_id,
            "image_url": result["image_url"],
            "title": edition["title"],
            "author": edition["author"],
            "publisher": edition["publisher"],
            "year": edition["year"],
            "pages": edition["pages"],
            "files": edition["files"]
        }

        enriched_results.append(enriched_result)

    return enriched_results

def download_file(f_id):
    file = get_file(f_id)
    
    if file is None:
        raise ValueError(f"File {f_id} not found")
    
    for file_id, file in file.items():
        #print(file.keys())
        print("File ID:", file_id)
        print("MD5:", file["md5"])
        print("Filesize:", file["filesize"])
        print("Extension:", file["extension"])
        print("Libgen ID:", file["libgen_id"])


        editions = file["editions"]
        e_id = next(iter(editions.values()))["e_id"]
        print("Edition ID:", e_id)
        edition = get_edition(e_id)
        edition_title = edition["title"]
        print("Edition title:", edition_title)


        md5 = file["md5"]
        expected_size = int(file["filesize"])
        download_url = get_download_link(str(md5))
        print (f"Download URL: {download_url}")
        download_page = urljoin(base_url, page_extension + md5)
        print(f"Download page: {download_page}")

        response = session.get(download_url, headers={
            **headers, 
            "Referer": download_page
            },
            allow_redirects=True
        )

        print(response.status_code)
        print(response.url)
        print(response.headers.get("content-type"))
        print(response.headers.get("Content-Length"))


        destination = f"{edition_title}.{file['extension']}"
        print(f"destination: {destination}")

        with open(destination, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)




    
    #md5 = file["md5"]
    #print(f"MD5: {md5}")

#download_file(4604718)

#data = get_files(4604718, 4604719)
data = get_file(4604718)
#print(data)
#print('type:', type(data))

#print(search("The Kite Runner")[:16000])  # Print the first 500 characters of the search results for "The Kite Runner"
#search("The Kite Runner")

print(search("weapons of math destruction"))

'''

results = get_search_results("Weapons of Math Destruction")

for result in results:
    print(
        result["edition_id"],
        result["title"],
        result["author"],
        result["year"]
    )
#'''

'''
soup = BeautifulSoup(search("The Kite Runner"), "html.parser")
rows = soup.select("#tablelibgen tbody tr")

for row in rows:
    print('')
    print (row)
    print('')
    edition_id = row.select_one("a[href]")["href"].split("=")[-1]
    image_url = row.select_one("img[src]")["src"]
    title = row.select_one("td:nth-of-type(2) a").get_text(strip=True) if row.select_one("td:nth-of-type(2) a") else None
    author = row.select_one("td:nth-of-type(3)").get_text(strip=True)
    print("edition_id:", edition_id)
    print("image_url:", image_url)
    print("title:", title)
    print("author:", author)
    print('')
    #print(get_file(edition_id))
    print('')
#'''
'''
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
        print('')
        print("   - Edition title:", edition["title"])
        print("   - Edition cover url:", edition["cover_url"])
        print("   - Edition author:", edition["author"])
        print("   - Edition publisher:", edition["publisher"])
        print("   - Edition year:", edition["year"])
        print("   - Files", edition["files"])
        print('')

#'''    

'''
download_url = get_download_link(
    "58617b920f2d3cbfe35cfc168db42302"
)

print(download_url)

response = session.get(download_url, headers={
    **headers, 
    "Referer": download_page
    },
    allow_redirects=True
)

print(response.status_code)
print(response.url)
print(response.headers.get("content-type"))
print(response.headers.get("Content-Length"))

with open("The Kite Run", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

#'''

#for e_id, edition in editions.items():
    #print(e_id, edition["title"], edition["year"])
