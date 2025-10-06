
import os
import sys
import logging
import requests
import traceback
from bs4 import BeautifulSoup

suffix = "?q=con%3A"
prefix = "/concept.jsp?id="
path = os.path.join(os.getcwd(), "topics.jsp")
descriptor = open(path, "r")
soup = descriptor.read()
descriptor.close()
soup = BeautifulSoup(soup)
links = soup.find_all("a")
targets = []
concepts = []
index = 0
for link in links:
    if not (link.has_attr("href")):
        continue
    link = link["href"]
    if not (link.startswith(prefix)):
        continue
    targets.append(link)
while (index < len(targets)):
    link = targets[index]
    index += 1
    if (len(sys.argv) > 1):
        if not (link[len(prefix):] == sys.argv[1]):
            continue
    if (link[len(prefix):] in concepts):
        continue
    try:
        path = os.path.join(os.getcwd(), "html", link[len(prefix):]+".html")
        if not (os.path.exists(path)):
            print(path)
            response = requests.get("https://corpus.quran.com"+link)
            descriptor = open(path, "w")
            descriptor.write(response.text)
            descriptor.close()
        else:
            descriptor = open(path, "r")
            text = descriptor.read()
            descriptor.close()
            beau = BeautifulSoup(text)
            neighbors = beau.find_all("a")
            for neighbor in neighbors:
                if not (neighbor.has_attr("href")):
                    continue
                neighbor = neighbor["href"]
                if not (neighbor.startswith(prefix)):
                    continue
                if (neighbor[len(prefix):] in concepts):
                    continue
                if (os.path.exists(os.path.join(os.getcwd(), "html", neighbor[len(prefix):]+".html"))):
                    continue
                print(neighbor)
                targets.append(neighbor)
        path = os.path.join(os.getcwd(), "html", "search_0_"+link[len(prefix):]+".html")
        if not (os.path.exists(path)):
            print(path)
            response = requests.get("https://corpus.quran.com/search.jsp?q=con%3A"+link[len(prefix):])
            text = response.text
            descriptor = open(os.path.join(os.getcwd(), "html", os.path.basename(sys.argv[0])+".html"), "w")
            descriptor.write(text)
            descriptor.close()
            beau = BeautifulSoup(text)
            pages = beau.find_all("a")
            total = 0
            for page in pages:
                #print(page)
                if not (page.has_attr("href")):
                    continue
                page = page["href"]
                if not (page.startswith(suffix+link[len(prefix):])):
                    continue
                if not ("&page=" in page):
                    continue
                page = int(page[(page.rindex("=")+1):])
                if (page > total):
                    total = page
            if (total > 0):
                print(str(total))
                text = None
                for i in range(total):
                    try:
                        path = os.path.join(os.getcwd(), "html", "search_"+str(i)+"_"+link[len(prefix):]+".html")
                        response = requests.get("https://corpus.quran.com/search.jsp?q=con%3A"+link[len(prefix):]+"&page="+str(i+1))
                        descriptor = open(path, "w")
                        descriptor.write(response.text)
                        descriptor.close()
                    except:
                        logging.error(traceback.format_exc())
            if not (text == None):
                path = os.path.join(os.getcwd(), "html", "search_0_"+link[len(prefix):]+".html")
                descriptor = open(path, "w")
                descriptor.write(text)
                descriptor.close()
    except:
        logging.error(traceback.format_exc())
    concepts.append(link[len(prefix):])

