import json
from LinksCleaner import clearLinks

pages = list()


with open('Crawler\\CrawlData\\LinksToCrawl.json', 'r', encoding='latin-1') as file:
    pages = json.load(file)
    file.close()
    
size = len(pages)

print(f'Links loaded!  Cleaning [{size}] links')

pages = clearLinks(pages)

size = len(pages)

print(f'Links cleaned! Resulted [{size}] links')

with open('Crawler\\CrawlData\\LinksToCrawl.json', 'w', encoding='latin-1') as jsonFile:
    json.dump(pages, jsonFile, indent=4)
    jsonFile.close()
