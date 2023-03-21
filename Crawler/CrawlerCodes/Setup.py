import json
import sqlite3
import os

caminho_pasta = "Crawler\\"

for z in ['CrawlData', 'Errors', 'OldCrawls', 'UnstoredCrawls']:
    try:
        os.mkdir(caminho_pasta+z)
        print("Folder criado com sucesso!")
    except FileExistsError:
        print("Folder já existe!")
    except Exception as e:
        print("Erro ao criar folder:", e)
        exit(-1)

with open('Crawler\\CrawlData\\LinksToCrawl.json', 'w', encoding='latin-1') as jsonFile:
    json.dump(["https://www.wikipedia.org", "https://google.com"], jsonFile, indent=4, ensure_ascii=False)
    jsonFile.close()

with open('Crawler\\CrawlData\\StoredLinks.db', 'w', encoding='latin-1') as db:
    db.close()

conn = sqlite3.connect('Crawler\\CrawlData\\StoredLinks.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE "Links" (
	"ID"	INTEGER NOT NULL UNIQUE,
	"LINK"	TEXT NOT NULL UNIQUE,
	"FROM"	INTEGER,
	PRIMARY KEY("ID" AUTOINCREMENT)
)''')
results = cursor.fetchall()

conn.commit()
conn.close()