import requests
import json
from urllib.parse import urljoin

url = "https://pip.pypa.io/en/stable/searchindex.js"

response = requests.get(url)

print("Status:", response.status_code)

start = response.text.find("{")
end = response.text.rfind("}") + 1

index_data = response.text[start:end]

index = json.loads(index_data)
print(type(index))
print(index.keys())

doc_id = index["terms"]["python"][0]

print("Document ID:", doc_id)
print("Title:", index["titles"][doc_id])
print("Filename:", index["filenames"][doc_id])
print("Docname:", index["docnames"][doc_id])

def search(query):
    words = query.lower().split()

    if not words:
        return []

    document_sets = []

    for word in words:
        if word not in index["terms"]:
            return []

        document_sets.append(set(index["terms"][word]))

    results = document_sets[0]

    for documents in document_sets[1:]:
        results &= documents

    return sorted(results)


for doc_id in search("python pip"):
    print(
        index["titles"][doc_id],
        "|",
        index["docnames"][doc_id]
    )


'''response2 = requests.get(urljoin(url, index["docnames"][doc_id]))

print("Status:", response2.status_code)
print("URL:", response2.url)
print(response2.text[:200])  # Print the first 2000 characters of the response

'''