#!/bin/sh
python3 -m pip install -r $PWD/requirements.txt
#rm -rf $PWD/json
#rm -rf $PWD/html
mkdir -p $PWD/json
mkdir -p $PWD/html
python3 $PWD/topics.py
python3 $PWD/xhtml.py
python3 $PWD/ontology.py
fdp -Tsvg ontology.py.dot -o ontology.py.dot.svg

