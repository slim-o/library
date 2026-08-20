from urllib.parse import urljoin

from bs4 import BeautifulSoup

from api import base_url, session, headers
from api import get_file, get_edition, page_extension


def get_download_link(md5):

    download_page = urljoin(base_url, page_extension + md5)
    response = session.get(download_page, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")


    for link in soup.find_all("a", href=True):
        if link["href"].startswith("get.php?"):
            #print(link["href"])
            return urljoin(base_url, link["href"])


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

