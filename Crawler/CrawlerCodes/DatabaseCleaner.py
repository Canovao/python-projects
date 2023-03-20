import sqlite3

conn = sqlite3.connect('Crawler\\CrawlData\\StoredLinks.db')
cursor = conn.cursor()

cursor.execute('''SELECT Links.ID FROM Links GROUP BY Links.LINK HAVING COUNT(Links.LINK) > 1 ORDER BY Links.ID''')
results = cursor.fetchall()

while len(results) != 0:
    cursor.execute('''DELETE FROM Links WHERE Links.ID IN (SELECT Links.ID FROM Links GROUP BY Links.LINK HAVING COUNT(Links.LINK) > 1 ORDER BY Links.ID)''')
    results = cursor.fetchall()

    cursor.execute('''SELECT Links.ID FROM Links GROUP BY Links.LINK HAVING COUNT(Links.LINK) > 1 ORDER BY Links.ID''')
    results = cursor.fetchall()
    
    print(len(results))
    
    conn.commit()

conn.close()

print('FINISHED')
