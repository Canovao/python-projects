import json
import sqlite3

def feedCrawler():
    jsonData = list()
    
    with open('Crawler\\CrawlData\\LinksToCrawl.json', 'r', encoding='utf-8') as outfile:
        jsonData = json.load(outfile)
        outfile.close()
    
    conn = sqlite3.connect('Crawler\\CrawlData\\StoredLinks.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT "LINK" FROM Links WHERE Links."FROM" IS NOT NULL''')
    results = cursor.fetchall()

    alreadyStoredLinks = list()

    for row in results:
        alreadyStoredLinks.append(row[0])
    
    if len(alreadyStoredLinks) == 0:
        print('No links to feed')
        exit(-1)
        
    for z in alreadyStoredLinks:
        jsonData.append(z)

    with open('Crawler\\CrawlData\\LinksToCrawl.json', 'w', encoding='utf-8') as outfile:
        json.dump(jsonData, outfile, indent=4, ensure_ascii=False)
        outfile.close()

    cursor.execute('''UPDATE Links SET "FROM" = NULL WHERE Links."FROM" IS NOT NULL''')
    results = cursor.fetchall()

    conn.commit()
    conn.close()
        
    print("Crawler fed!")

if __name__ == "__main__":
    feedCrawler()
