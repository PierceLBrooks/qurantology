
import os
import sys
import json

names = {}
parents = {}
categories = {}
alternatives = {}
for root, folders, files in os.walk(os.path.join(os.getcwd(), "json")):
    for name in files:
        if not (name.endswith(".json")):
            continue
        path = os.path.join(root, name)
        name = name[:name.index(".")]
        descriptor = open(path, "r")
        content = descriptor.read()
        descriptor.close()
        data = json.loads(content)
        if not ("dict" in str(type(data))):
            continue
        if (sys.flags.debug):
            print(str(data))
        key = "name"
        if (key in data):
            if not (name in names):
                names[name] = data[key]
        key = "Parent category"
        if (key in data):
            if not (name in parents):
                parents[name] = []
            if ("str" in str(type(data[key]))):
                parents[name].append(data[key])
            else:
                for datum in data[key]:
                    parents[name].append(datum)
        key = "Categories"
        if (key in data):
            if not (name in categories):
                categories[name] = []
            if ("str" in str(type(data[key]))):
                categories[name].append(data[key])
            else:
                for datum in data[key]:
                    categories[name].append(datum)
        key = "Alternative names"
        if (key in data):
            if not (name in alternatives):
                alternatives[name] = []
            if ("str" in str(type(data[key]))):
                alternatives[name].append(data[key])
            else:
                for datum in data[key]:
                    alternatives[name].append(datum)
    break
arrays = []
arrays.append(parents)
arrays.append(categories)
arrays.append(alternatives)
descriptor = open(os.path.join(os.getcwd(), os.path.basename(sys.argv[0])+".dot"), "w")
descriptor.write("digraph G {\n")
nodes = {}
for array in arrays:
    for key in array:
        if (key in nodes):
            continue
        nodes[key] = len(nodes)
for array in arrays:
    for key in array:
        for i in range(len(array[key])):
            node = array[key][i]
            if not (node in nodes):
                nodes[node] = len(nodes)
            descriptor.write("\tnode"+str(nodes[key])+" -> node"+str(nodes[node])+";\n")
for node in nodes:
    if (node in names):
        descriptor.write("\tnode"+str(nodes[node])+" [ label = \""+names[node]+"\" ] ;\n")
    else:
        descriptor.write("\tnode"+str(nodes[node])+" [ label = \""+node+"\" ] ;\n")
descriptor.write("}\n")
descriptor.close()

