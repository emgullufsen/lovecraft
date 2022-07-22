#!/usr/bin/python3.9
import requests
from bs4 import BeautifulSoup

url = "https://www.hplovecraft.com/writings/texts/"
page = requests.get("https://www.hplovecraft.com/writings/texts/")
parser = BeautifulSoup(page.text, 'html.parser')
uls = parser.find_all('ul')
fiction_list = uls[0].find_all('ul')[0].find_all('a')
print(fiction_list)

for book in fiction_list[1:]:
    name = book.contents[0]
    link = url + book.get('href')
    print(name)
    print(link)