from bs4 import BeautifulSoup
import requests

url = 'https://www.recipe-free.com/recipes/easy-swedish-meatballs---jamie-oliver-recipe/129381'

result = requests.get(url).text

doc = BeautifulSoup(result, 'html.parser')

heading = doc.find('div', class_= 'col-md-12 for-padding-col')
#ingredients = doc.find()
p_tags = heading.find_all('p')
ingredients = []
for elem in p_tags:
    p_links = elem.find_all('p')
for i in p_links:
    ingredients.append(i.text)
print(ingredients)
