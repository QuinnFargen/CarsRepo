
import requests
import Scraper.config
import random 
from bs4 import BeautifulSoup
from scraper_api import ScraperAPIClient
import Scraper.header

class Scrap():

    def __init__(self, Domain):
        self.headers = Scraper.header.headers_list
        self.Domain = Domain

    def get_soup_safe(self,carURL):
        client = ScraperAPIClient(Scraper.config.scraper_APIKey)
        result = client.get(url = carURL).text
        return BeautifulSoup(result, 'html.parser')

    def get_soup_spicy(self,carURL,refURL):
        if refURL == '':
            if self.Domain == 'CDC':
                refURL = 'https://www.cars.com/'
            else: 
                refURL = 'https://www.edmunds.com/'
        header = random.choice(self.headers)
        header["Referer"] = refURL
        r = requests.get(carURL, headers=header)
        return BeautifulSoup(r.text, 'html.parser')

    def get_soup(self,carURL,useCase,refURL=''):
        if useCase == 'IDs' or useCase == 'spicy':
            return self.get_soup_spicy(carURL,refURL)
        elif useCase == 'Car':
            return self.get_soup_safe(carURL)


