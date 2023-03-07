
from Scraper.CarsScrap import get_soup

carURL = 'https://www.edmunds.com/toyota/camry/2019/vin/4T1B11HK1KU788019/?radius=25'

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
    soup = get_soup(carURL, 'Car')
    attr = {}     
    if soup.find('p', attrs={'class': 'sds-notification__desc'}) is not None:
        if soup.find('p', attrs={'class': 'sds-notification__desc'}).text == 'Sorry, this vehicle is no longer available.':
            return {'Status': 'No Longer'}  # When Car Not Listed   # <p class="sds-notification__desc">Sorry, this vehicle is no longer available.</p>
        # Pull out individual values
        # <section class="vin-overview my-1_5 my-md-1 px-0_25 px-md-0 text-gray-darker" data-tracking-parent="edm-entry-vin-overview">
        # <div class="d-flex justify-content-between align-items-center"><div><div class="text-gray-darker medium">Used</div>
        # <h1 class="d-inline-block mb-0 heading-2 mt-0_25">2019 Toyota Camry</h1>
        # <div class="text-gray-darkest font-weight-normal mt-0_25">LE 4dr Sedan (2.5L 4cyl 8A)</div></div><div class="d-none d-lg-flex flex-column align-items-center" data-tracking-parent="edm-entry-qr-code"><canvas style="height:96px;width:96px" height="192" width="192"></canvas><img src="https://static.ed.edmunds-media.com/unversioned/icons/logo/Edmunds-logomark.svg" style="display:none"><span class="small text-gray-darker mt-0_25" aria-hidden="true">View on your phone</span><a href="https://www.edmunds.com/toyota/camry/2019/vin/4T1B11HK1KU788019/?radius=25&amp;utm_source=edmunds&amp;utm_medium=qr_code&amp;utm_targetId=917876da-2836-4a17-8c0f-37c14316a5b6" class="sr-only sr-only-focusable small" rel="nofollow">QR Code: <!-- -->View on your phone</a></div></div></section>
    vinOverview = soup.find('section', attrs={'class': 'vin-overview my-1_5 my-md-1 px-0_25 px-md-0 text-gray-darker'})
    attr["new_used"] = vinOverview.find('div', attrs={'class': 'text-gray-darker medium'}).text
    attr["listing_title"] = vinOverview.find('h1', attrs={'class': 'd-inline-block mb-0 heading-2 mt-0_25'}).text
    attr["trim_engine"] = vinOverview.find('div', attrs={'class': 'text-gray-darkest font-weight-normal mt-0_25'}).text
        # <span class="" data-test="vdp-price-row" data-testid="vdp-price-row">$15,911</span>
    attr["primary_price"] = soup.find('span', attrs={'data-testid': 'vdp-price-row'}).text
    # <div class="d-flex deal-image scroll-link heading-5 text-lowercase align-items-center text-nowrap great"><i class="mr-1 size-16 align-middle icon-icon-great-price text-great"></i>Great<!-- --> price</div>
    # <div class="align-self-end label text-nowrap text-info text-gray-dark">$5,584 Below Market<div class="d-inline-block"><div class="deal-popover d-inline-block"><sup class="ml-0_25 top-0 size-10 align-middle"><i id="tooltipdeal-type-tooltip" role="tooltip" aria-label="Tooltip of deal type" aria-describedby="tooltipdeal-type-tooltip-sr-content" tabindex="0" class="icon-info info-popover-icon"></i><span id="tooltipdeal-type-tooltip-sr-content" class="sr-only"><span class="d-block disclaimer-popover"><span class="content-fragment d-block mb-1 medium font-weight-bold">Edmunds considers this used vehicle a <span>Great Price</span> because the savings is $5,584 Below Market.</span><span class="d-block m-0 medium">15% of the used inventory currently listed on Edmunds is a great price.  <!-- -->Our ratings are accurate and up-to-date – we've analyzed thousands of similar transactions and listings to rate these deals.</span></span></span></sup></div></div></div>
    if soup.find('div', attrs={'class': 'd-flex deal-image scroll-link heading-5 text-lowercase align-items-center text-nowrap great'}).text == 'Great price':
        belowabove = soup.find('div', attrs={'class': 'align-self-end label text-nowrap text-info text-gray-dark'}).text 
        if belowabove.find(' Below Market') is not None:
            attr["secondary_price"] = soup.find('div', attrs={'class': 'align-self-end label text-nowrap text-info text-gray-dark'}).text.split(" Below Market")[0]
        else:
            attr["secondary_price"] = soup.find('div', attrs={'class': 'align-self-end label text-nowrap text-info text-gray-dark'}).text.split(" Above Market")[0]
    
    
    # Nested values find
    fancy_desc = soup.find('dl', attrs={'class': 'fancy-description-list'})
    if fancy_desc.find('span') is not None:
        fancy_desc.span.decompose()    
    dt = fancy_desc.find_all('dt')
    dd = fancy_desc.find_all('dd')
    # Ind and Nested values into dicts

        # listing_mileage

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
