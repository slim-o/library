# search_default()

from libgen_api_enhanced import LibgenSearch
s = LibgenSearch(mirror="li")
results = s.search_default("Pride and Prejudice") # a list of Book objects