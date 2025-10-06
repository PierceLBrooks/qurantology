
import os
import sys
import json
import logging
import requests
import traceback
import xml.etree.ElementTree as xml_tree
from bs4 import BeautifulSoup

def handle(node, parent, level, clazzism):
    prefix = "/concept.jsp?id="
    result = None
    tag = node.tag.lower().strip()
    #print(("  "*level)+tag)
    if (tag == "table"):
        result = {}
        for child in node:
            data = handle(child, node, level+1, clazzism)
            if ("dict" in str(type(data))):
                for key in data:
                    result[key] = data[key]
            else:
                if (len(result) == 0):
                    result = []
                if ("list" in str(type(result))):
                    for key in data:
                        result.append(key)
    elif (tag == "tr"):
        key = None
        children = {}
        for child in node:
            child = handle(child, node, level+1, clazzism)
            if (key == None):
                key = child
            else:
                if ("dict" in str(type(key))):
                    #print(str(key))
                    for keys in key:
                        children[keys] = key[keys]
                elif ("list" in str(type(key))):
                    #print(str(key))
                    result = key
                else:
                    children[key] = child
                key = None
        if (result == None):
            if not (key == None):
                try:
                    for child in key:
                        children[child] = key[child]
                except:
                    pass
            return children
    elif (tag == "td"):
        if ((clazzism) and ("class" in node.attrib)):
            if ("property" == node.attrib["class"].lower().strip()):
                return node.text.strip().replace(u'\xa0', u' ')
            result = {}
            result[str(node.attrib["class"])] = node.text.strip()
        if (result == None):
            result = []
            for child in node:
                data = handle(child, node, level+1, clazzism)
                if not (data == None):
                    result.append(data)
            if (len(result) == 0):
                result.append(node.text.strip())
    elif (tag == "a"):
        if ("href" in node.attrib):
            if (node.attrib["href"].startswith(prefix)):
                return node.attrib["href"][len(prefix):].replace(u'\xa0', u' ')
        return node.text.strip().replace(u'\xa0', u' ')
    elif (tag == "span"):
        result = node.text.strip().replace(u'\xa0', u' ')
    else:
        print(tag)
    return result

temps = {}
temps["Category"] = "Categories"
temps["Alternative name"] = "Alternative names"
temps["Son"] = "Sons"
keys = []
post = ""
for root, folders, files in os.walk(os.path.join(os.getcwd(), "html")):
    for name in files:
        if (name.startswith("search_")):
            continue
        if not (name.endswith(".html")):
            continue
        path = os.path.join(root, name)
        descriptor = open(path, "r")
        soup = descriptor.read()
        descriptor.close()
        try:
            soup = BeautifulSoup(soup)
            tables = soup.find_all("table")
            for table in tables:
                if not (table.has_attr("class")):
                    continue
                clazz = table["class"]
                if not ("infoBox" in clazz):
                    #print(name)
                    #print(clazz)
                    continue
                html = str(table.prettify())
                path = os.path.join(os.getcwd(), os.path.basename(sys.argv[0])+".xml")
                #print(path)
                descriptor = open(path, "w")
                descriptor.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
                descriptor.write(html)
                descriptor.close()
                #sys.exit()
                tree = xml_tree.parse(path)
                base = tree.getroot()
                data = handle(base, None, 0, True)
                temp = []
                for key in data:
                    if (key in temps):
                        temp.append(key)
                for key in temp:
                    value = data[key]
                    del data[key]
                    data[temps[key]] = value
                for key in data:
                    if not (key in keys):
                        keys.append(key)
                pres = soup.find_all("pre")
                for pre in pres:
                    data["pre"] = pre.text
                    post += "\n"+pre.text+"\n"
                    break
                data["verses"] = []
                index = 0
                while (True):
                    path = os.path.join(os.getcwd(), "html", "search_"+str(index)+"_"+name)
                    index += 1
                    if (os.path.exists(path)):
                        descriptor = open(path, "r")
                        soup = descriptor.read()
                        descriptor.close()
                        soup = BeautifulSoup(soup)
                        those = soup.find_all("table")
                        for this in those:
                            if not (this.has_attr("class")):
                                continue
                            clazz = this["class"]
                            if not ("taf" in clazz):
                                #print(name)
                                #print(clazz)
                                continue
                            html = str(this.prettify())
                            path = os.path.join(os.getcwd(), os.path.basename(sys.argv[0])+".xml")
                            #print(path)
                            descriptor = open(path, "w")
                            descriptor.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
                            descriptor.write(html)
                            descriptor.close()
                            tree = xml_tree.parse(path)
                            base = tree.getroot()
                            verses = handle(base, None, 0, False)
                            for verse in verses:
                                data["verses"].append(verse)
                            break
                    else:
                        break
                descriptor = open(os.path.join(os.getcwd(), "json", name[:name.index(".")]+".json"), "w")
                descriptor.write(json.dumps(data))
                descriptor.close()
                break
        except:
            logging.error(traceback.format_exc())
    break
for key in keys:
    print(key)
descriptor = open(os.path.join(os.getcwd(), "pre.txt"), "w")
descriptor.write(post)
descriptor.close()

