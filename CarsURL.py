
def addAND(param):
    if param == '':
        return ''
    return param + '&'

def carsDotCom_Single(id):
    return 'https://www.cars.com/vehicledetail/' + id + '/'

def carsDotCom_Multi(page=1,pgsize='100',make='',model='',trim='',yrmin='',yrmax='',mile='',type='all',sort='best_match_desc',maxdist='all',zip='57106'):
    baseURL = 'https://www.cars.com/shopping/results/?'
    _page = 'page=' + str(page)
    if page == 0:
        _page = ''
    _pgsize = 'page_size=' + str(pgsize)
    _make = 'makes[]=' + make
    _model = 'models[]=' + model
    _trim = 'trims[]=' + trim
    _yrmin = 'year_max=' + yrmin
    _yrmax = 'year_min=' + yrmax

    _mile = 'mileage_max=' + mile  # 10000, by 10K, 100000, 150000, 200000, 250000, blank for any
    _type = 'stock_type=' + type # all, used, new_cpo, new, cpo
    _sort = 'sort=' + sort  # best_match_desc, list_price, list_price_desc, mileage, mileage_desc, distance, best_deal, year_desc, year, listed_at_desc, listed_at
    _maxdist = 'maximum_distance=' + maxdist   # all, 500, 250, 100, 50


    _zip = 'zip=' + zip
    websiteURL = addAND(_page) + addAND(_pgsize) + addAND(_sort) + addAND(_maxdist)
    carURL = addAND(_make) + addAND(_model) + addAND(_trim) + addAND(_yrmin) + addAND(_yrmax) + addAND(_mile) + addAND(_type)
    return baseURL + websiteURL + carURL  + _zip



# carsDotCom_Multi(page=5,pgsize=50,make='toyota',model='toyota-camry',trim='toyota-camry-se',yrmin='2018',yrmax='2018',mile='',type='used',sort='list_price',maxdist='all',zip='57193')
# carsDotCom_Multi(page=0,make='toyota',model='toyota-camry',zip='57193')

# '''
# page1 = 'https://www.cars.com/shopping/results/?dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=toyota&maximum_distance=all&mileage_max=&models[]=toyota-camry&page_size=20&sort=best_match_desc&stock_type=used&trims[]=toyota-camry-se&year_max=2018&year_min=2018&zip=57193'
# page1 = 'https://www.cars.com/shopping/results/?
#     dealer_id=
#     &keyword=
#     &list_price_max=
#     &list_price_min=
#     &makes[]=toyota
#     &maximum_distance=all
#     &mileage_max=
#     &models[]=toyota-camry
#     &page_size=20
#     &sort=best_match_desc
#     &stock_type=used
#     &trims[]=toyota-camry-se
#     &year_max=2018
#     &year_min=2018
#     &zip=57193'


# page2 = 'https://www.cars.com/shopping/results/?page=2&page_size=20&dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=toyota&maximum_distance=all&mileage_max=&models[]=toyota-camry&sort=best_match_desc&stock_type=used&trims[]=toyota-camry-se&year_max=2018&year_min=2018&zip=57193'
# page2 = 'https://www.cars.com/shopping/results/?
#     page=2
#     &page_size=20
#     &dealer_id=
#     &keyword=
#     &list_price_max=
#     &list_price_min=
#     &makes[]=toyota
#     &maximum_distance=all
#     &mileage_max=
#     &models[]=toyota-camry
#     &sort=best_match_desc
#     &stock_type=used
#     &trims[]=toyota-camry-se
#     &year_max=2018
#     &year_min=2018
#     &zip=57193'


# https://www.cars.com/shopping/results/?dealer_id=&keyword=
# &list_price_max=&list_price_min=&maximum_distance=all&mileage_max=&page_size=50
# &sort=list_price

# &stock_type=all&year_max=&year_min=&zip=57193


# '''