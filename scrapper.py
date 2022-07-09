from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests

url = 'https://www.recipe-free.com/recipes/easy-swedish-meatballs---jamie-oliver-recipe/129381'

result = requests.get(url).text

doc = BeautifulSoup(result, 'html.parser')
title = doc.find('h1', {'class': 'red'}).text.strip()
ingredients = doc.find('div', {'class': 'col-md-12 for-padding-col'}).find_all('p')[0].text.strip()
servings = doc.find('div', {'class': 'times'}).findAll('div', {'class': 'times_tab'})[1].findAll('div', {'class': 'f12 f12'})[1].text.strip()
instructions = doc.find('div', {'class': 'col-md-12 for-padding-col'}).find_all('p')[1].text.strip()
print(title)
print(ingredients)
print(servings)
print(instructions)
