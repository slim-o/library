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

download_file(4604718)

#data = get_files(4604718, 4604719)
data = get_file(4604718)
#print(data)
#print('type:', type(data))

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
