#!/usr/bin/python3.9
import requests
from bs4 import BeautifulSoup

url = "https://www.hplovecraft.com/writings/texts/"
page = requests.get("https://www.hplovecraft.com/writings/texts/")
parser = BeautifulSoup(page.text, 'html.parser')
print(page.text)
