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
import argparse

# My functions/classes
from StoreCrawl import storeCrawl
from LinksCleaner import clearLinks
from Feeder import feedCrawler
from StoreError import storeError

# initialCrawl = ["https://www.wikipedia.org", "https://google.com"]


parser = argparse.ArgumentParser()
parser.add_argument("--crawlSize", help="How much links the Crawler will crawl", type=int)
args = parser.parse_args()

now = datetime.now()
today = date.today()
current_time = now.strftime("%H-%M-%S")

csvPath = 'Crawler\\UnstoredCrawls\\CrawlerLinks'+str(today)+'--'+current_time+'.csv'

csvFile = csv.writer(open(csvPath, 'w', encoding="utf-8"))
csvFile.writerow(['From Link', "Gotten Links"])

storeAndFeed = True

with open('Crawler\\CrawlData\\LinksToCrawl.json', 'w+r', encoding='latin-1') as file:
    pages = json.load(file)
   
    if args.arg1 > 0:
        if args.arg1 > len(pages):
            args.arg1 = len(pages)
        
        json.dump(pages[args.arg1:], file)
        
        pages = pages[:args.arg1]
        storeAndFeed = False
       
    file.close()

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
                
            soup = BeautifulSoup(page.text, 'html.parser')

            aTags = soup.find_all('a')
            links = list()
            for tag in aTags:
                if tag.get('href') != None or tag.get('href') != "#":
                    links.append(tag.get('href'))

            cleanLinks = clearLinks(item, links)
            
            try:
                semaforo.acquire()
                csvFile.writerow([item, cleanLinks])
                semaforo.release()
            except UnicodeEncodeError as error:
                storeError(error, "Unicode Encode Error: ")
                continue
        except TypeError as error:
            storeError(error, 'Type error: ')
            continue
        except Exception as exception:
            storeError(error, 'Generic exception: ')
            continue

semaforo = threading.Semaphore(1)

if len(pages) >= 12:
    tamanhoParte = len(pages) // 4
    
    parte1 = pages[0:tamanhoParte]
    parte2 = pages[tamanhoParte:tamanhoParte*2]
    parte3 = pages[tamanhoParte*2:tamanhoParte*3]
    parte4 = pages[tamanhoParte*3:len(pages)]
    
    thread1 = threading.Thread(target=crawl, args=(parte1,1,))
    thread2 = threading.Thread(target=crawl, args=(parte2,2,))
    thread3 = threading.Thread(target=crawl, args=(parte3,3,))
    thread4 = threading.Thread(target=crawl, args=(parte4,4,))

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
else:
    crawl(pages)

if storeAndFeed == True:
    sleep(1)

    storeCrawl()

    feedCrawler()
