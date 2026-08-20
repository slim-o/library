from bs4 import BeautifulSoup

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