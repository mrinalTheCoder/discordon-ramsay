from requests_html import HTMLSession
from bs4 import BeautifulSoup

async def get_elements_from_tag(tag):
	d = {}
	d['name'] = tag['title']
	d['link'] = tag['href']
	div = tag.findChildren("img", recursive=True)[0]
	d['img'] = div['src'][len('https://imagesvc.meredithcorp.io/v3/mm/image?url='):]
	return d

async def search_recipe(a):
	a.replace(" ", "+")
	searchURL="https://www.allrecipes.com/search/results/?search="+a
	session = HTMLSession()
	response = session.get(searchURL)
	response.html.render(timeout=30)
	soup = BeautifulSoup(response.html.html, "html.parser")
	Title = soup.find_all("a", {"class":"card__titleLink manual-link-behavior"})
	x = Title[:10:2]
	x = list(map(get_elements_from_tag, x))
	return x
