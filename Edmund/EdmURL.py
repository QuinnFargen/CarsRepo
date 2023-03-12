

def Url_Single(_allfour):
    return 'https://www.edmunds.com/' + _allfour[0] + '/' + _allfour[1] + '/' + _allfour[2] + '/vin/' + _allfour[3]


def Url_Multi(_page=1,_make='',_model='',_trim='',_yrmin='',_yrmax='',_mile='',_type='used%2Ccpo%2Cnew'):
    baseURL = 'https://www.edmunds.com/inventory/srp.html?'
    page = 'pagenumber=' + str(_page)
    if _page == 0:
        page = ''
    make = 'make=' + _make
    model = 'model=' + _model
    if _trim == '':
        trim = ''
    else:
        trim = 'trims=' + _trim
    if _yrmin == '' or _yrmax == '':
        yr = ''
    else:
        yr = 'year=' + _yrmin + '-' + _yrmax

    mile = 'mileage=*-' + _mile  # 10000, by 10K, 100000, 150000, 200000, 250000, blank for any
    type = 'inventorytype=' + _type # all, used, new_cpo, new, cpo
    zip = 'radius=6000'

    websiteURL = addAND(page)
    carURL = addAND(make) + addAND(model) + addAND(trim) + addAND(yr) + addAND(mile) + addAND(type)
    return baseURL + websiteURL + carURL  + zip


##############################################
## Suplemental functions

def addAND(param):
    if param == '':
        return ''
    return param + '&'




# https://www.edmunds.com/inventory/srp.html?inventorytype=used&make=toyota&model=camry&radius=6000
# https://www.edmunds.com/inventory/srp.html?inventorytype=used&make=toyota&model=camry&radius=6000&pagenumber=2
# https://www.edmunds.com/inventory/srp.html?inventorytype=used&make=toyota&model=camry&radius=6000&trim=camry%7Cse&year=2019-2022
# https://www.edmunds.com/inventory/srp.html?inventorytype=used&make=toyota&model=camry&radius=6000&trim=camry%7Cse&year=2019-*
# https://www.edmunds.com/inventory/srp.html?inventorytype=used%2Ccpo%2Cnew&make=toyota&model=camry&radius=6000&trim=camry%7Cse&year=2019-*&mileage=*-176000

# https://www.edmunds.com/toyota/camry/2019/vin/4T1B11HK1KU276387/?radius=6000





