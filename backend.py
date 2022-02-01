import lxml
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

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
    searchURL = "https://www.allrecipes.com/search/results/?search=" + a
    response = requests.get(searchURL)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    Title = soup.find_all("a", {"class": "card__titleLink"})
    x = Title[:10:2]
    x = list(map(get_elements_from_tag, x))
    description = soup.find_all('div', {'class': 'card__summary'})
    description = list(map(lambda inp:inp.get_text().strip(), description))
    print(description)
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


search_recipe(input())
