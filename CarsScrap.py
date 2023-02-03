
import requests
import config
from bs4 import BeautifulSoup
from scraper_api import ScraperAPIClient


def get_soup_safe(carURL):
    client = ScraperAPIClient(config.scraper_APIKey)
    result = client.get(url = carURL).text
    return BeautifulSoup(result, 'html.parser')

def get_soup_spicy(carURL):
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4040.128"}
    r = requests.get(carURL) #, headers=header, timeout=5)
    return BeautifulSoup(r.text, 'html.parser')



def get_soup(carURL, useCase):
    if useCase == 'IDs':
        return get_soup_spicy(carURL)
    elif useCase == 'Car':
        return get_soup_safe(carURL)
        
