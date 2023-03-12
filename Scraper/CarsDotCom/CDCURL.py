

def C_Url_Single(id):
    return 'https://www.cars.com/vehicledetail/' + id + '/'

def C_Url_Multi(_page=1,_pgsize='100',_make='',_model='',_trim='',_yrmin='',_yrmax='',_mile='',_type='all',_sort='best_match_desc',_maxdist='all',_zip='57106'):
    baseURL = 'https://www.cars.com/shopping/results/?'
    page = 'page=' + str(_page)
    if _page == 0:
        page = ''
    pgsize = 'page_size=' + str(_pgsize)
    make = 'makes[]=' + _make
    model = 'models[]=' + _model
    if _trim is None:
        trim = ''
    else:
        trim = 'trims[]=' + _trim
    if _yrmin == '0':
        yrmin = ''; yrmax = ''
    else:
        yrmin = 'year_max=' + _yrmin
        yrmax = 'year_min=' + _yrmax

    mile = 'mileage_max=' + _mile  # 10000, by 10K, 100000, 150000, 200000, 250000, blank for any
    type = 'stock_type=' + _type # all, used, new_cpo, new, cpo
    sort = 'sort=' + _sort  # best_match_desc, list_price, list_price_desc, mileage, mileage_desc, distance, best_deal, year_desc, year, listed_at_desc, listed_at
    maxdist = 'maximum_distance=' + _maxdist   # all, 500, 250, 100, 50


    zip = 'zip=' + _zip
    websiteURL = addAND(page) + addAND(pgsize) + addAND(sort) + addAND(maxdist)
    carURL = addAND(make) + addAND(model) + addAND(trim) + addAND(yrmin) + addAND(yrmax) + addAND(mile) + addAND(type)
    return baseURL + websiteURL + carURL  + zip

##############################################
## Suplemental functions

def addAND(param):
    if param == '':
        return ''
    return param + '&'







# carsDotCom_Multi(page=5,pgsize=50,make='toyota',model='toyota-camry',trim='toyota-camry-se',yrmin='2018',yrmax='2018',mile='',type='used',sort='list_price',maxdist='all',zip='57193')
# carsDotCom_Multi(page=0,make='toyota',model='toyota-camry',zip='57193')


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
