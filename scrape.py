#!/usr/bin/python3.9
import requests
from bs4 import BeautifulSoup
from time import sleep as t_sleep
import re

marker = "<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>"
req_headers = {
    'User-Agent': 'Eric Gullufsen, rickysquid.org',
    'From': 'ericgullufsen@gmail.com'
}
url = "https://www.hplovecraft.com/writings/texts/"
page = requests.get(url, headers=req_headers)
if (not page.ok):
    print("couldn't retrieve base page")
    exit(1)
parser = BeautifulSoup(page.text, 'html.parser')
uls = parser.find_all('ul')
fiction_list = uls[0].find_all('ul')[0].find_all('a')

for book in fiction_list:
    name = book.contents[0]
    name_cleansed = re.sub(r'[^\w\s]','',name)
    name_cleansed = name_cleansed.replace(' ','_')
    link = book.get('href')
    resp = requests.get(url + link, headers=req_headers)
    if resp.status_code == 200:
        parser2 = BeautifulSoup(resp.text, 'html.parser')
        trs2 = parser2.find_all('tr')
        the_row = trs2[4]
        print(marker)
        print(repr(name))
        print(marker)
        t = ' '.join(the_row.stripped_strings)
        print(t)
        print("\n\n\n")
        with open("corpus/" + name_cleansed + ".txt", 'w') as w_file:
            w_file.write(t)