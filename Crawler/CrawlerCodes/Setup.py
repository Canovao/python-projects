import sqlite3
import os

nome_pasta = "CrawlData"
caminho_pasta = "Crawler\\" + nome_pasta

try:
    os.mkdir(caminho_pasta)
    print("Folder criado com sucesso!")
except FileExistsError:
    print("Folder já existe!")
except Exception as e:
    print("Erro ao criar folder:", e)
    exit(-1)

with open('Crawler\\CrawlData\\LinksToCrawl.json', 'w', encoding='latin-1') as jsonFile:
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