

import os
import requests
from datetime import date
from bs4 import BeautifulSoup


cars_url = 'https://www.cars.com/shopping/results/?dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=toyota&maximum_distance=all&mileage_max=&models[]=toyota-camry&page_size=20&sort=best_match_desc&stock_type=used&trims[]=toyota-camry-se&year_max=2018&year_min=2018&zip=57193'

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4040.128"}
r = requests.get(cars_url) #, headers=header, timeout=5)
soup = BeautifulSoup(r.text, 'html.parser')
# scripttext = soup.find('vehicle-cards').getText()
cont = soup.find("div", {"id": "vehicle-cards-container"})
scripttext = soup.getText()
conttext = cont.getText()

content_list = soup.find_all('div', attrs={'class': 'vehicle-cards'})
print(content_list)

dt = date.today().strftime("%Y_%m_%d %H:%M:%S")
FileName = dt + '_' + 'Toyata' + '_' + 'Camry' + '_' + '2018' + ".html"
writeTxt = open(FileName, "w")
writeTxt.write(cont.text)
writeTxt.close()

