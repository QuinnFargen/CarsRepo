
from bs4 import BeautifulSoup
from Scraper.CarsScrap import get_soup


def Scrap_IDs(carURL):
    soup = get_soup(carURL, 'IDs')
        #Getting all divs with an id name starting with vehicle-card
    vehicleIDs = soup.findAll('div', id=lambda x: x and x.startswith('vehicle-card-'))
    IDs = []    #Get all the ID values, strip off additional text from ID
    for i in range(len(vehicleIDs)):
        for ID in vehicleIDs[i].find_all('div', id=True):  
            if '-lead-btns' in ID.get('id'):
                extra = ID.get('id')
                IDs.append(extra.replace('-lead-btns','').replace('sponsored-',''))
    tot_entries = soup.find('span', attrs={'class': 'total-entries'}).text
    numEntry = int(''.join(i for i in tot_entries if i.isdigit()))
    return [IDs,numEntry]


def Scrap_Car(carURL):
    soup = get_soup(carURL, 'Car')
    attr = {}     
    if soup.find('p', attrs={'class': 'sds-notification__desc'}) is not None:
        if soup.find('p', attrs={'class': 'sds-notification__desc'}).text == 'Sorry, this vehicle is no longer available.':
            return {'Status': 'No Longer'}  # When Car Not Listed   # <p class="sds-notification__desc">Sorry, this vehicle is no longer available.</p>
        # Pull out individual values
    attr["new_used"] = soup.find('p', attrs={'class': 'new-used'}).text
    attr["listing_title"] = soup.find('h1', attrs={'class': 'listing-title'}).text
    attr["listing_mileage"] = soup.find('div', attrs={'class': 'listing-mileage'}).text
    attr["primary_price"] = soup.find('span', attrs={'class': 'primary-price'}).text
    if soup.find('span', attrs={'class': 'secondary-price price-drop'}) is not None:
        attr["secondary_price"] = soup.find('span', attrs={'class': 'secondary-price price-drop'}).text
    # Nested values find
    fancy_desc = soup.find('dl', attrs={'class': 'fancy-description-list'})
    if fancy_desc.find('span') is not None:
        fancy_desc.span.decompose()    
    dt = fancy_desc.find_all('dt')
    dd = fancy_desc.find_all('dd')
    # Ind and Nested values into dicts
    known = ['Exterior color', 'Interior color', 'Drivetrain', 'Fuel type', 'Transmission', 'Engine', 'VIN', 'Mileage']
    label = ['Ext_Color','Int_Color','Drivetrain','Fuel','Trans','Engine','VIN','Mileage']
    for d in range(len(dt)):
        if dt[d].text in known:
            i = known.index(dt[d].text)
            attr[label[i]] = dd[d].text.strip()
    return attr



# cars_url = 'https://www.cars.com/shopping/results/?dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=toyota&maximum_distance=all&mileage_max=&models[]=toyota-camry&page_size=20&sort=best_match_desc&stock_type=used&trims[]=toyota-camry-se&year_max=2018&year_min=2018&zip=57193'
# cars_url = 'https://www.cars.com/shopping/results/?page=2&page_size=20&dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=toyota&maximum_distance=all&mileage_max=&models[]=toyota-camry&sort=best_match_desc&stock_type=used&trims[]=toyota-camry-se&year_max=2018&year_min=2018&zip=57193'
# Scrap_IDs(cars_url)

#     #Exists
# carURL = 'https://www.cars.com/vehicledetail/dec1cb07-a7f2-41d6-a60c-659e670db63f/'
#     #BADDDDD
# carURL = 'https://www.cars.com/vehicledetail/6313112d-5f5e-4b8e-b751-57bfcd331f96/'

# attr = Scrap_Car(carURL)
# attr
