import os

from bs4 import BeautifulSoup
import requests
#from IPython.display import Image, display

#url = 'https://www.recipe-free.com/recipes/easy-swedish-meatballs---jamie-oliver-recipe/129381'
#url = 'https://www.recipe-free.com/categories/meat-recipes/1'

#result = requests.get(url).text

#doc = BeautifulSoup(result, 'html.parser')


#title = doc.find('h1', {'class': 'red'}).text.strip()
#ingredients = doc.find('div', {'class': 'col-md-12 for-padding-col'}).find_all('p')[0].text.strip()
#servings = doc.find('div', {'class': 'times'}).findAll('div', {'class': 'times_tab'})[1].findAll('div', {'class': 'f12 f12'})[1].text.strip()
#instructions = doc.find('div', {'class': 'col-md-12 for-padding-col'}).find_all('p')[1].text.strip()
#print(f'title: {title}')
#print(f'ingredients: {ingredients}')
#print(f'servings: {servings}')
#print(f'instructions: {instructions}')


page = 1
url_no = 1
titles = []
links = []
links_dict = {}
#url_link = 1
while page != 7:
    url = f"https://www.recipe-free.com/categories/meat-recipes/{page}"
    #print(url)
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "lxml")
    for a in soup.find('div', {'class': 'category_content centerindent for-this'}).findAll('a', {'class': 'day'}):
        titles.append(a.get_text(strip=True))
        links.append(a.get('href'))
        #print(titles)
    page = page + 1
for title in titles[:80]:
    print(title)
for i, link in enumerate(links[:120], url_no):
    #print(f'url {url_no}: {link}')
    name = f'url {url_no}'
    links_dict = {name : link}
    #links_dict = {f'url {url_no}': link}
    url_no += 1
    #for dict in links_dict:
    #print(links_dict)
    print(links_dict[name])
    #code to get info from each link stored in links_dict
    url_grapper = links_dict[name]
    result = requests.get(url_grapper).text    
    doc = BeautifulSoup(result, 'html.parser')
    # Extract image URL
    image_tag = doc.find('div', {'class': 'col-md-4 col-sm-4'}).findAll('div')[0].findAll('img')[0]
    image_url = image_tag['src']
    image_url_fixed = image_url.replace('../..', '')
    base_url = 'https://www.recipe-free.com'
    rimage_url = base_url + image_url_fixed
    try:
        rimage = requests.get(rimage_url).content  # Fetch image data
    except requests.exceptions.RequestException as e:
        print(f"Error! Failed to fetch image from {rimage_url}: {e}")
        rimage = None


    # Extract other recipe details
    title = doc.find('h1', {'class': 'red'}).text.strip()
    ingredients = doc.find('div', {'class': 'col-md-12 for-padding-col'}).find_all('p')[0].text.strip()
    servings = doc.find('div', {'class': 'times'}).findAll('div', {'class': 'times_tab'})[1].findAll('div', {'class': 'f12 f12'})[1].text.strip()
    instructions = doc.find('div', {'class': 'col-md-12 for-padding-col'}).find_all('p')[1].text.strip()

    #print(f'title: {title}')
    #print(f'ingredients: {ingredients}')
    #print(f'servings: {servings}')
    #print(f'instructions: {instructions}')
    print(f'image: {rimage_url}')



        #print(f"{links_dict['url']}")
#for link in links[:120]:
    #while url_link <= 8:
        #print(f'Url {url_link}: {link}')
        #url_link = url_link + 1



