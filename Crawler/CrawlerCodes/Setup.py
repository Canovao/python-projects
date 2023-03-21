import sqlite3

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