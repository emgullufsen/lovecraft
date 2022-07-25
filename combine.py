#!/usr/bin/python3
from os import listdir
from os.path import join

COMBINED_FILENAME = "all.txt"
data = ''

for filename in listdir("corpus"):
    with open(join("corpus", filename), 'r', encoding="UTF-8") as f:
        text = f.read()
        data += text

with open(join("corpus", COMBINED_FILENAME), 'w', encoding="UTF-8") as o:
    o.write(data)
