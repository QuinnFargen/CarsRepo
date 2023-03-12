
from Scraper.CarsScrap import get_soup


def Scrap_href(carURL):
    soup = get_soup(carURL, 'spicy')
    hrefs = []
    for link in soup.findAll('a'):
        if '/vin/' in link.get('href'):
            hrefs.append(link.get('href'))
    tot_entries = soup.find('span', attrs={'class': 'inventory-count'}).text
    numEntry = int(''.join(i for i in tot_entries if i.isdigit()))
    return list(set(hrefs)), numEntry

def Scrap_IDs(carURL):
    hrefs, numEntry = Scrap_href(carURL)
    IDs = []; indices = [1,2,3,5]
    for h in range(len(hrefs)):
        IDs.append(list(map(lambda x: hrefs[h].split('/')[x],indices)))
    return [IDs,numEntry]


def Scrap_Car(carURL):
    soup = get_soup(carURL, 'spicy')
    attr = {}     
    if soup.find('h2', attrs={'class': 'pt-1 pt-md-3 px-1 px-md-3 pb-2 text-center display-1 m-0'}) is not None:
        return {'Status': 'No Longer'}  # When Car Not Listed   # <p class="sds-notification__desc">Sorry, this vehicle is no longer available.</p>
        # Pull out individual Top values
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
        # Loop thru table/matrix bottom values
    VehicleSum = soup.find('section', attrs={'class': 'vehicle-summary w-100 text-gray-darker'})  
    li = VehicleSum.find_all('li')
        #Text box trailers that mess with split between Key/Value
    remove = ['Based on model year EPA mileage ratings. Use for comparison purposes only. Your mileage will vary depending on how you drive and maintain your vehicle, driving conditions, battery-pack age/condition and other factors.','Based on default model values and available option information. Contact dealer to confirm.']
    known = ['Mileage','Ext. ColorExterior color ','Int. ColorInterior color ','Engine','Transmission','Drivetrain','MPG','Horsepower','Seats','VIN','Stock #']
    label = ['Mileage','Ext_Color','Int_Color','Fuel','Trans','Drivetrain','MPG','HP','Seats','VIN','Stock']
    for d in range(len(li)):
        attrText = li[d].text.replace(remove[0],'').replace(remove[1],'')
        for k in range(len(known)):
            if len( attrText.split(known[k]) ) > 1:
                labelIndex = k
        attr[label[labelIndex]] = attrText.split(known[labelIndex])[1]

    return attr


# cars_url = 'https://www.cars.com/shopping/results/?dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=toyota&maximum_distance=all&mileage_max=&models[]=toyota-camry&page_size=20&sort=best_match_desc&stock_type=used&trims[]=toyota-camry-se&year_max=2018&year_min=2018&zip=57193'
# cars_url = 'https://www.cars.com/shopping/results/?page=2&page_size=20&dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=toyota&maximum_distance=all&mileage_max=&models[]=toyota-camry&sort=best_match_desc&stock_type=used&trims[]=toyota-camry-se&year_max=2018&year_min=2018&zip=57193'
# carURL = 'https://www.edmunds.com/inventory/srp.html?inventorytype=used%2Ccpo&make=honda&model=civic&radius=6000'

    #Exists
# carURL = 'https://www.cars.com/vehicledetail/dec1cb07-a7f2-41d6-a60c-659e670db63f/'
# carURL = 'https://www.edmunds.com/honda/civic/2008/vin/1HGFA15578L001577/?radius=100'
#     #BADDDDD
# carURL = 'https://www.cars.com/vehicledetail/6313112d-5f5e-4b8e-b751-57bfcd331f96/'
# carURL = 'https://www.edmunds.com/toyota/camry/2019/vin/4T1B11HK1KU788019/?radius=25'
