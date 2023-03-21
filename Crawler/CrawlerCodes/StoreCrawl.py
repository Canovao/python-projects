import csv
import sqlite3
import sys
import glob
import tqdm

maxInt = sys.maxsize

while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

def storeCrawl():
    paths = glob.glob('Crawler\\UnstoredCrawls\\*.csv')
    for csvData in paths:
        print('Storaging .csv data')
        
        rows = list()

        if not csvData.endswith(".csv"):
            print('File in Unstored Crawls is not a .csv file')
            continue

        with open(csvData, newline='', encoding="utf-8") as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',', quotechar='"')
            for row in csvReader:
                if len(row) != 0:
                    rows.append(row)
            csvFile.close()
        
        print(csvData, rows)
        
        if len(rows) == 0:
            print("No data to store!")
            continue

        del rows[0]

        for z in range(len(rows)):
            string = rows[z][1]
            string_sem_aspas = string.strip('\"')
            lista = eval(string_sem_aspas)
            rows[z][1] = lista

        conn = sqlite3.connect('Crawler\\CrawlData\\StoredLinks.db')
        cursor = conn.cursor()

        for z in range(len(rows)):
            if rows[z][0].endswith("/"):
                rows[z][1] = rows[z][1][0:len(rows[z][1])-1]

            cursor.execute('''INSERT OR IGNORE INTO "main"."Links" ("LINK") VALUES (?)''', (rows[z][0],))

            cursor.execute('SELECT "ID" FROM "main"."Links" WHERE "LINK" = ?', (rows[z][0],))

            last_id = cursor.fetchone()[0]
            
            for x in range(len(rows[z][1])):
                if rows[z][1][x] != '':
                    if rows[z][1][x].endswith("/"):
                        rows[z][1][x] = rows[z][1][x][0:len(rows[z][1][x])-1]
                        
                    cursor.execute('''INSERT OR IGNORE INTO "main"."Links" ("LINK", "FROM") VALUES (?, ?)''', (rows[z][1][x], last_id,))

        results = cursor.fetchall()

        conn.commit()
        print("CSV data stored!")
