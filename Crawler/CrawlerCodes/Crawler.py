from bs4 import BeautifulSoup
from datetime import datetime
from datetime import date
from tqdm import tqdm
from time import sleep
import threading
import json
import re
import string
import requests
import csv

# My functions/classes
from StoreCrawl import storeCrawl
from LinksCleaner import clearLinks
from Feeder import feedCrawler
from StoreError import storeError

# initialCrawl = ["https://www.wikipedia.org", "https://google.com"]

now = datetime.now()
today = date.today()
current_time = now.strftime("%H-%M-%S")

csvPath = 'Crawler\\UnstoredCrawls\\CrawlerLinks'+str(today)+'--'+current_time+'.csv'

storeAndFeed = True

with open('Crawler\\CrawlData\\LinksToCrawl.json', 'r', encoding='latin-1') as file:
    pages = json.load(file)
    
    pageAmount = 0
    
    if len(pages) > 100:
        pageAmount = int(input(f"Insert how many link you wanna crawl [max {len(pages)}]: "))
   
    if pageAmount > 0:
        file.close()
        
        if pageAmount != len(pages):
            storeAndFeed = False
        
        with open('Crawler\\CrawlData\\LinksToCrawl.json', 'w', encoding='latin-1') as jsonFile:
            json.dump(pages[pageAmount:], jsonFile, indent=4)
            jsonFile.close()
        
        pages = pages[:pageAmount]

csvFile = csv.writer(open(csvPath, 'w', encoding="utf-8"))
csvFile.writerow(['From Link', "Gotten Links"])

def crawl(pageList: list(), threadNum: int = 0):
    global csvFile
    
    for i in tqdm(range(0, len(pageList)), ncols = 150, desc =f"Thread {threadNum} / Crawled pages: "):
        try:    
            item = pageList[i]
            
            try:
                page = requests.get(item)
            except requests.exceptions.ConnectTimeout as error:
                storeError(error, 'Conexion timeout ERROR: ', threadNum)
                continue
            except requests.exceptions.ConnectionError as error:
                storeError(error, 'Conexion ERROR: ', threadNum)
                continue
            except requests.exceptions.ReadTimeout as error:
                storeError(error, 'Read timeout ERROR: ', threadNum)
                continue
            except requests.exceptions.InvalidURL as error:
                storeError(error, 'Invalid URL exception: ', threadNum)
                continue
            except Exception as error:
                storeError(error, 'Generic request exception: ', threadNum)
                continue
                
            soup = BeautifulSoup(page.text, 'html.parser')

            aTags = soup.find_all('a')
            links = list()
            for tag in aTags:
                if tag.get('href') != None or tag.get('href') != "#":
                    links.append(tag.get('href'))

            cleanLinks = clearLinks(links, item)
            
            try:
                semaforo.acquire()
                csvFile.writerow([item, cleanLinks])
                semaforo.release()
            except UnicodeEncodeError as error:
                storeError(error, "Unicode Encode Error: ", threadNum)
                continue
        except TypeError as error:
            storeError(error, 'Type error: ', threadNum)
            continue
        except Exception as error:
            storeError(error, 'Generic exception: ', threadNum)
            continue

semaforo = threading.Semaphore(1)

if len(pages) >= 24:
    tamanhoParte = len(pages) // 8
    
    parte1 = pages[0:tamanhoParte]
    parte2 = pages[tamanhoParte:tamanhoParte*2]
    parte3 = pages[tamanhoParte*2:tamanhoParte*3]
    parte4 = pages[tamanhoParte*3:tamanhoParte*4]
    parte5 = pages[tamanhoParte*4:tamanhoParte*5]
    parte6 = pages[tamanhoParte*5:tamanhoParte*6]
    parte7 = pages[tamanhoParte*6:tamanhoParte*7]
    parte8 = pages[tamanhoParte*7:len(pages)]
    
    thread1 = threading.Thread(target=crawl, args=(parte1,1,))
    thread2 = threading.Thread(target=crawl, args=(parte2,2,))
    thread3 = threading.Thread(target=crawl, args=(parte3,3,))
    thread4 = threading.Thread(target=crawl, args=(parte4,4,))
    thread5 = threading.Thread(target=crawl, args=(parte5,5,))
    thread6 = threading.Thread(target=crawl, args=(parte6,6,))
    thread7 = threading.Thread(target=crawl, args=(parte7,7,))
    thread8 = threading.Thread(target=crawl, args=(parte8,8,))

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()
    thread7.start()
    thread8.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
    thread6.join()
    thread7.join()
    thread8.join()
else:
    crawl(pages)

if storeAndFeed == True:
    sleep(1)

    storeCrawl()

    feedCrawler()
