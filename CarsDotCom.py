

'''
https://www.cars.com/shopping/results/?dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=toyota&maximum_distance=all&mileage_max=50000&models[]=toyota-camry&page_size=20&sort=best_match_desc&stock_type=used&year_max=2018&year_min=2018&zip=57193

https://www.cars.com/shopping/results/?
    dealer_id=
    &keyword=
    &list_price_max=
    &list_price_min=
    &makes[]=toyota
    &maximum_distance=all
    &mileage_max=50000
    &models[]=toyota-camry
    &page_size=20
    &sort=best_match_desc
    &stock_type=used
    &year_max=2018
    &year_min=2018
    &zip=57193

    &trims[]=toyota-camry-se


------------------------
Wants:
    search systematically
    increment page in loop
    get how many matches to estimate how many pages
    get IDs of cars for direct url to cars
    get VINs

'''
import os
import requests
from datetime import date
from bs4 import BeautifulSoup


cars_url = 'https://www.cars.com/shopping/results/?dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=toyota&maximum_distance=all&mileage_max=&models[]=toyota-camry&page_size=20&sort=best_match_desc&stock_type=used&trims[]=toyota-camry-se&year_max=2018&year_min=2018&zip=57193'
# x = requests.get(cars_url)
# print(x)
# print(x.text)


header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4040.128"}
r = requests.get(cars_url) #, headers=header, timeout=5)
soup = BeautifulSoup(r.text, 'html.parser')
# scripttext = soup.find('vehicle-cards').getText()
scripttext = soup.getText()


dt = date.today().strftime("%Y_%m_%d")
FileName = dt + '_' + 'Toyata' + '_' + 'Camry' + '_' + '2018' + ".txt"
writeTxt = open(FileName, "w")
writeTxt.write(scripttext)
writeTxt.close()