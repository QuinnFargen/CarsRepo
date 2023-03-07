
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
    return IDs, numEntry


def Scrap_Car(carURL):
    soup = get_soup(carURL, 'spicy')
    attr = {}     
        # Add check logic if car doesn' exist:
    # if soup.find('p', attrs={'class': 'sds-notification__desc'}) is not None:
    #     if soup.find('p', attrs={'class': 'sds-notification__desc'}).text == 'Sorry, this vehicle is no longer available.':
    #         return {'Status': 'No Longer'}  # When Car Not Listed   # <p class="sds-notification__desc">Sorry, this vehicle is no longer available.</p>
        # Pull out individual values
    vinOverview = soup.find('section', attrs={'class': 'vin-overview my-1_5 my-md-1 px-0_25 px-md-0 text-gray-darker'})
    attr["new_used"] = vinOverview.find('div', attrs={'class': 'text-gray-darker medium'}).text
    attr["listing_title"] = vinOverview.find('h1', attrs={'class': 'd-inline-block mb-0 heading-2 mt-0_25'}).text
    attr["trim_engine"] = vinOverview.find('div', attrs={'class': 'text-gray-darkest font-weight-normal mt-0_25'}).text
    attr["primary_price"] = soup.find('span', attrs={'data-testid': 'vdp-price-row'}).text
    if soup.find('div', attrs={'class': 'd-flex deal-image scroll-link heading-5 text-lowercase align-items-center text-nowrap great'}).text == 'Great price':
        belowabove = soup.find('div', attrs={'class': 'align-self-end label text-nowrap text-info text-gray-dark'}).text 
        if belowabove.find(' Below Market') is not None:
            attr["secondary_price"] = soup.find('div', attrs={'class': 'align-self-end label text-nowrap text-info text-gray-dark'}).text.split(" Below Market")[0]
        else:
            attr["secondary_price"] = soup.find('div', attrs={'class': 'align-self-end label text-nowrap text-info text-gray-dark'}).text.split(" Above Market")[0]
    
    VehicleSum = soup.find('section', attrs={'class': 'vehicle-summary w-100 text-gray-darker'})  
    li = VehicleSum.find_all('li')
        #Text box trailers that mess with split between Key/Value
    remove0 = 'Based on model year EPA mileage ratings. Use for comparison purposes only. Your mileage will vary depending on how you drive and maintain your vehicle, driving conditions, battery-pack age/condition and other factors.'
    remove1 = 'Based on default model values and available option information. Contact dealer to confirm.'

    known = ['Mileage','Ext. ColorExterior color ','Int. ColorInterior color ','Engine','Transmission','Drivetrain','MPG','Horsepower','Seats','VIN','Stock #']
    label = ['Mileage','Ext_Color','Int_Color','Fuel','Trans','Drivetrain','MPG','HP','Seats','VIN','Stock']
    for d in range(len(li)):
        attrText = li[d].text.replace(remove0,'').replace(remove1,'')
        for k in range(len(known)):
            if len( attrText.split(known[k]) ) > 1:
                labelIndex = k
        attr[label[labelIndex]] = attrText.split(known[labelIndex])[1]

    return attr


# cars_url = 'https://www.cars.com/shopping/results/?dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=toyota&maximum_distance=all&mileage_max=&models[]=toyota-camry&page_size=20&sort=best_match_desc&stock_type=used&trims[]=toyota-camry-se&year_max=2018&year_min=2018&zip=57193'
# cars_url = 'https://www.cars.com/shopping/results/?page=2&page_size=20&dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=toyota&maximum_distance=all&mileage_max=&models[]=toyota-camry&sort=best_match_desc&stock_type=used&trims[]=toyota-camry-se&year_max=2018&year_min=2018&zip=57193'
# Scrap_IDs(cars_url)

#     #Exists
# carURL = 'https://www.cars.com/vehicledetail/dec1cb07-a7f2-41d6-a60c-659e670db63f/'
# carURL = 'https://www.edmunds.com/toyota/camry/2019/vin/4T1B11HK1KU788019/?radius=25'
#     #BADDDDD
# carURL = 'https://www.cars.com/vehicledetail/6313112d-5f5e-4b8e-b751-57bfcd331f96/'

# attr = Scrap_Car(carURL)
# attr
