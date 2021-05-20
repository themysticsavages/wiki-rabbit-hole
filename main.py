import sys
import requests 
import bs4 
import os
import random
import time

local = '\\'.join(__file__.split('\\')[0:-1])
os.chdir(local)

if os.path.isdir('content') == True:
    os.chdir('content')
else:
    os.mkdir('content')
    os.chdir('content')

index = 0
items = []

def WikiLoop(url):
    global index
    res = requests.get(url)
    wiki = bs4.BeautifulSoup(res.text, 'html.parser')

    for i in wiki.select('p'):
        items.append(i.getText())
    indexx = 0
    with open('file'+str(index)+'.txt', 'w', encoding='utf-8') as file:
        for item in items:
            file.write(items[indexx])
            indexx += 1

    allLinks = wiki.find(id="bodyContent").find_all("a")
    title = wiki.find(id="firstHeading")

    print('Scraping '+str(title.string)+'...', end=' ')
    random.shuffle(allLinks)
    scrapelink = 0

    for link in allLinks:
        # We are only interested in other wiki articles
        if link['href'].find("/wiki/") == -1: 
            continue

        # Use this link to scrape
        scrapelink = link
        break
    
    items.clear()
    index += 1
    
    print('Done')
    time.sleep(0.5)
    try:
        WikiLoop('https://en.wikipedia.org' + scrapelink['href'])
    except Exception:
        exit(0)

WikiLoop('https://en.wikipedia.org/wiki/'+sys.argv[1])