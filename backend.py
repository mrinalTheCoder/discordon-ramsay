import requests
from bs4 import BeautifulSoup
import random

def get_elements_from_tag(tag):
	d = {}
	d['name'] = tag['title']
	d['link'] = tag['href']
	div = tag.findChildren("img", recursive=True)[0]
	d['img'] = div['src'][len('https://imagesvc.meredithcorp.io/v3/mm/image?url='):]
	return d

def search_recipe(a):
	a.replace(" ", "+")
	searchURL = "https://www.allrecipes.com/search/results/?search=" + a
	response = requests.get(searchURL)
	content = response.content
	soup = BeautifulSoup(content, "html.parser")
	Title = soup.find_all("a", {"class": "card__titleLink"})
	x = Title[:10:2]
	x = list(map(get_elements_from_tag, x))
	description = soup.find_all('div', {'class': 'card__summary'})
	description = list(map(lambda inp:inp.get_text().strip(), description))
	for i in range(len(x)):
		x[i]['desc'] = description[i]
	return x

def get_recipe_details(d):
	response = requests.get(d['link'])
	content = response.content
	soup = BeautifulSoup(content, "html.parser")
	ingredients = soup.find('ul', {'class': 'ingredients-section'}).findChildren('li')
	final_list = []
	for i in ingredients:
		label = i.findChildren('label')[0].findChildren('input')[0]
		final_list.append(f'{label["data-quantity"]} {label["data-unit"]} {label["data-ingredient"]}')

	instructions = soup.find('ul', {'class': 'instructions-section'}).findChildren('li')
	instructions = list(map(lambda x: x.findChildren('p', recursive=True)[0].get_text(), instructions))
	return {'ing': final_list, 'steps': instructions}

def random_meal(meal_page_link, inds=list(range(8))):
	response=requests.get(meal_page_link)
	content=response.content
	soup = BeautifulSoup(content, "html.parser")
	Title = soup.find_all("a", {"class": "card__titleLink"})
	x = Title[::2]
	x = [x[i] for i in inds]
	x = list(map(get_elements_from_tag, x))
	descriptions = soup.find_all('div', {'class': 'card__summary'})[:max(inds)]
	descriptions = list(map(lambda inp: inp.get_text().strip(), descriptions))
	for i in range(len(x)):
		x[i]['desc'] = descriptions[i]

	num = random.randint(0, len(inds)-1)

	link = x[num]['link']
	response = requests.get(link)
	content = response.content
	soup = BeautifulSoup(content, "html.parser")
	ingredients = soup.find('ul', {'class': 'ingredients-section'}).findChildren('li')
	final_list = []
	for i in ingredients:
		label = i.findChildren('label')[0].findChildren('input')[0]
		final_list.append(f'{label["data-quantity"]} {label["data-unit"]} {label["data-ingredient"]}')
	instructions = soup.find('ul', {'class': 'instructions-section'}).findChildren('li')
	instructions = list(map(lambda x: x.findChildren('p', recursive=True)[0].get_text(), instructions))
	return x[num], {'ing': final_list, 'steps': instructions}

def random_bfast():
	bfast="https://www.allrecipes.com/recipes/78/breakfast-and-brunch/"
	return random_meal(bfast)

def random_lunch():
    lunch="https://www.allrecipes.com/recipes/17561/lunch/"
    return random_meal(lunch)

def random_dinner():
    dinner="https://www.allrecipes.com/recipes/17562/dinner/"
    return random_meal(dinner)

def random_drink():
	drinks="https://www.allrecipes.com/recipes/77/drinks/"
	return random_meal(drinks, inds=[0, 1, 2, 4, 5, 7, 8, 9])

def random_dessert():
	dessert = "https://www.allrecipes.com/recipes/79/desserts/"
	return random_meal(dessert, inds=[1, 3, 4, 5, 6, 8, 9, 10])
