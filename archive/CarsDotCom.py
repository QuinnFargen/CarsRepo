

#######################

# USED FOR TESTING

########################




import os
import requests
from datetime import date
from bs4 import BeautifulSoup


cars_url = 'https://www.cars.com/shopping/results/?dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=toyota&maximum_distance=all&mileage_max=&models[]=toyota-camry&page_size=20&sort=best_match_desc&stock_type=used&trims[]=toyota-camry-se&year_max=2018&year_min=2018&zip=57193'
cars_url = 'https://www.cars.com/shopping/results/?page=2&page_size=20&dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=toyota&maximum_distance=all&mileage_max=&models[]=toyota-camry&sort=best_match_desc&stock_type=used&trims[]=toyota-camry-se&year_max=2018&year_min=2018&zip=57193'

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4040.128"}
r = requests.get(cars_url) #, headers=header, timeout=5)
soup = BeautifulSoup(r.text, 'html.parser')


vehicleIDs = soup.findAll('div', id=lambda x: x and x.startswith('vehicle-card-'))


IDs = []
for i in range(len(vehicleIDs)):
    for ID in vehicleIDs[i].find_all('div', id=True):  
        if '-lead-btns' in ID.get('id'):
            extra = ID.get('id')
            IDs.append(extra.replace('-lead-btns','').replace('sponsored-',''))
len(IDs)



import requests
from bs4 import BeautifulSoup


carURL = 'https://www.cars.com/vehicledetail/6313112d-5f5e-4b8e-b751-57bfcd331f96/'

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4040.128"}
r = requests.get(carURL) #, headers=header, timeout=5)
soup = BeautifulSoup(r.text, 'html.parser')


new_used = soup.find('p', attrs={'class': 'new-used'}).text
listing_title = soup.find('h1', attrs={'class': 'listing-title'}).text
listing_mileage = soup.find('div', attrs={'class': 'listing-mileage'}).text

new_used, listing_title, listing_mileage


primary_price = soup.find('span', attrs={'class': 'primary-price'}).text
secondary_price = soup.find('span', attrs={'class': 'secondary-price price-drop'}).text

primary_price, secondary_price



fancy_desc = soup.find('dl', attrs={'class': 'fancy-description-list'})
fancy_desc.span.decompose()
dt = fancy_desc.find_all('dt')
dd = fancy_desc.find_all('dd')
# Put them into a dictionary

dd[1].text

desc[0].text

for s in fancy_desc.select('span'):
    s.extract()

len(vehicleIDs)

vehicleIDs[0]
vehicleIDs[1]

vehicleIDs.get('id')
vehicleIDs[2].find_all(id=True)

# scripttext = soup.find('vehicle-cards').getText()
cont = soup.find("div", {"id": "vehicle-cards-container"})
scripttext = soup.getText()
conttext = cont.getText()

content_list = soup.find_all('div', attrs={'class': 'vehicle-cards'})
content_list = soup.find_all('div', attrs={'class': 'vehicle-card'})
print(content_list)

dt = date.today().strftime("%Y_%m_%d %H:%M:%S")
FileName = dt + '_' + 'Toyata' + '_' + 'Camry' + '_' + '2018' + ".html"
writeTxt = open(FileName, "w")
writeTxt.write(cont.text)
writeTxt.close()

