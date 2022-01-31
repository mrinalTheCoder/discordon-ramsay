import requests
from bs4 import BeautifulSoup

def get_elements_from_tag(tag):
	d = {}
	d['name'] = tag['title']
	d['link'] = tag['href']
	div = tag.findChildren("img", recursive=True)[0]
	d['img'] = div['src'][len('https://imagesvc.meredithcorp.io/v3/mm/image?url='):]
	return d

def search_recipe(a):
	a.replace(" ", "+")
	searchURL="https://www.allrecipes.com/search/results/?search="+a
	response = requests.get(searchURL)
	content = response.content
	soup = BeautifulSoup(content, "html.parser")
	#print(soup)
	#Title = soup.find_all("a", {"class":"card__titleLink manual-link-behavior"})
	Title = soup.find_all("a", {"class":"card__titleLink"})
	#print(Title)
	x = Title[:10:2]
	x = list(map(get_elements_from_tag, x))
	return x
