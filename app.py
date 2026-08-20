from search import search
from api import get_edition
from downloader import download_file

query = input("Search: ")

results = search(query)

for i, result in enumerate(results, start=1):

    print(
        f"[{i}] "
        f"{result['title']} - "
        f"{result['author']}"
    )

choice = int(input("\nSelect result: "))

selected = results[choice - 1]

edition = get_edition(selected["edition_id"])

print("\nTitle:", edition["title"])
print("Author:", edition["author"])
print("Publisher:", edition["publisher"])
print("Year:", edition["year"])
print(edition)