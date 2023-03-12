
class Website():

    def __init__(self,Domain):
        self.Domain = Domain

    def Url_Single(self,_id='',_allfour=[]):
        if _id != '':
            return 'https://www.cars.com/vehicledetail/' + _id + '/'
        return 'https://www.edmunds.com/' + _allfour[0] + '/' + _allfour[1] + '/' + _allfour[2] + '/vin/' + _allfour[3]

    # params = ['https://www.cars.com/shopping/results/?','','makes[]=toyota']
    def paramComb(self, pars=[]):
        url = '&'.join(pars)
        while '&&' in url:
            url = url.replace('&&','&')
        return url
    
    def paramNone(self,par,pre=''):
        if par == None:
            return ''
        if pre != '':
            return pre + str(par)
        return str(par)
  
    def Url_Multi(self,_make,_model,_trim,_yrmin,_yrmax,_page=1,_pgsize='100',_mile='',_type='all',_sort='best_match_desc',_maxdist='all'):
        if self.Domain == 'CDC':
            baseURL = 'https://www.cars.com/shopping/results/?'
            page = 'page=' + str(_page)
            if _page == 0:
                page = ''
            pgsize = 'page_size=' + str(_pgsize)
            make = 'makes[]=' + _make
            model = self.paramNone(_make+'-'+_model, pre='models[]=')
            trim = self.paramNone(_make+'-'+_model+'-'+_trim, pre='trims[]=')
            yrmin = self.paramNone(_yrmin, pre='year_min=')
            yrmax = self.paramNone(_yrmax, pre='year_max=')
            mile = 'mileage_max=' + _mile  # 10000, by 10K, 100000, 150000, 200000, 250000, blank for any
            type = 'stock_type=' + _type # all, used, new_cpo, new, cpo
            sort = 'sort=' + _sort  # best_match_desc, list_price, list_price_desc, mileage, mileage_desc, distance, best_deal, year_desc, year, listed_at_desc, listed_at
            maxdist = 'maximum_distance=' + _maxdist   # all, 500, 250, 100, 50
            zip = 'zip=57106'
            pars = [baseURL,page,pgsize,sort,maxdist,make,model,trim,yrmin,yrmax,mile,type,zip]
            Murl = self.paramComb(pars)
            return Murl
        else:   #Edmunds
            baseURL = 'https://www.edmunds.com/inventory/srp.html?'
            page = 'pagenumber=' + str(_page)
            if _page == 0:
                page = ''
            make = 'make=' + _make
            model = 'model=' + _model
            trim = trim = 'trims=' + self.paramNone(_trim)
            if self.paramNone(_yrmin) == '' or self.paramNone(_yrmax) == '':
                yr = ''
            else:
                yr = 'year=' + _yrmin + '-' + _yrmax
            mile = 'mileage=*-' + _mile  # 10000, by 10K, 100000, 150000, 200000, 250000, blank for any
            if _type == 'all':
                _type = 'used%2Ccpo%2Cnew'
            type = 'inventorytype=' + _type # all, used, new_cpo, new, cpo
            zip = 'radius=6000'
            pars = [baseURL,page,make,model,trim,yr,mile,type,zip]
            Murl = self.paramComb(pars)
            return Murl
        
    def Scrap_href(self,soup):
        hrefs = []
        for link in soup.findAll('a'):
            if '/vin/' in link.get('href'):
                hrefs.append(link.get('href'))
        tot_entries = soup.find('span', attrs={'class': 'inventory-count'}).text
        numEntry = int(''.join(i for i in tot_entries if i.isdigit()))
        return list(set(hrefs)), numEntry

    def Scrap_IDs(self,soup):
        if self.Domain == 'CDC':
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
        else: 
            hrefs, numEntry = self.Scrap_href(soup)
            IDs = []; indices = [1,2,3,5]
            for h in range(len(hrefs)):
                IDs.append(list(map(lambda x: hrefs[h].split('/')[x],indices)))
            return [IDs,numEntry]

    def Scrap_Car(self,soup):
        if self.Domain == 'CDC':
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
        else:
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





# Url = 'https://www.edmunds.com/inventory/srp.html?inventorytype=used%2Ccpo&make=honda&model=civic&radius=6000'
# E = Edmund()
# E.get_allLinks(Url)

# Url = 'https://www.cars.com/shopping/results/?stock_type=used&makes%5B%5D=honda&models%5B%5D=honda-civic&list_price_max=&maximum_distance=all&zip=57193'
# C = CarsCom()
# C.get_allLinks(Url)



