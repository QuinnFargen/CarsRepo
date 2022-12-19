
import requests
from bs4 import BeautifulSoup

def Scrap_IDs(carsURL):
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4040.128"}
    r = requests.get(carsURL) #, headers=header, timeout=5)
    soup = BeautifulSoup(r.text, 'html.parser')
        
        #Getting all divs with an id name starting with vehicle-card
    vehicleIDs = soup.findAll('div', id=lambda x: x and x.startswith('vehicle-card-'))

        #Get all the ID values, strip off additional text from ID
    IDs = []
    for i in range(len(vehicleIDs)):
        for ID in vehicleIDs[i].find_all('div', id=True):  
            if '-lead-btns' in ID.get('id'):
                extra = ID.get('id')
                IDs.append(extra.replace('-lead-btns','').replace('sponsored-',''))

    tot_entries = soup.find('span', attrs={'class': 'total-entries'}).text
    numEntry = int(''.join(i for i in tot_entries if i.isdigit()))

    return IDs, numEntry



def Scrap_Car(carURL):
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4040.128"}
    r = requests.get(carURL) #, headers=header, timeout=5)
    soup = BeautifulSoup(r.text, 'html.parser')

    new_used = soup.find('p', attrs={'class': 'new-used'}).text
    listing_title = soup.find('h1', attrs={'class': 'listing-title'}).text
    listing_mileage = soup.find('div', attrs={'class': 'listing-mileage'}).text

    primary_price = soup.find('span', attrs={'class': 'primary-price'}).text
    secondary_price = soup.find('span', attrs={'class': 'secondary-price price-drop'}).text

    fancy_desc = soup.find('dl', attrs={'class': 'fancy-description-list'})
    fancy_desc.span.decompose()
    dt = fancy_desc.find_all('dt')
    dd = fancy_desc.find_all('dd')

    attr = {'new_used': new_used, 'listing_title' : listing_title, 'listing_mileage': listing_mileage, 'prim_price': primary_price, 'sec_price': secondary_price}
    desc = {}
    if len(dt) ==  10:
        desc = {'Ext Color': dd[0].text, 'Int Color': dd[1].text, 'Drivetrain': dd[2].text, 'Fuel': dd[4].text, 'Trans': dd[5].text
                , 'Engine': dd[6].text, 'VIN': dd[7].text, 'Stock': dd[8].text, 'Mileage': dd[9].text}

    return attr, desc

    # Put them into a dictionary


    # new_used, listing_title, listing_mileage
    # primary_price, secondary_price







# cars_url = 'https://www.cars.com/shopping/results/?dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=toyota&maximum_distance=all&mileage_max=&models[]=toyota-camry&page_size=20&sort=best_match_desc&stock_type=used&trims[]=toyota-camry-se&year_max=2018&year_min=2018&zip=57193'
# cars_url = 'https://www.cars.com/shopping/results/?page=2&page_size=20&dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=toyota&maximum_distance=all&mileage_max=&models[]=toyota-camry&sort=best_match_desc&stock_type=used&trims[]=toyota-camry-se&year_max=2018&year_min=2018&zip=57193'
# Scrap_IDs(cars_url)
# carURL = 'https://www.cars.com/vehicledetail/b0209b5d-5562-4396-b25e-8e77152ad30d/'
# Scrap_Car('https://www.cars.com/vehicledetail/6313112d-5f5e-4b8e-b751-57bfcd331f96/')