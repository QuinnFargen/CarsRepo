

from CarsURL import Url_Multi, Url_Single
from CarsScrap import Scrap_IDs, Scrap_Car

from CarsDB import log_ScrapLog, log_ScrapMeta, log_Vehicle, get_MMTrim, get_VINs
from time import sleep



def Loop_ManyMulti():
    MMT_All = get_MMTrim(_MMTID=0)
    for i in range(MMT_All.shape[0]):
        MMT, _make, _model, _trim = get_MMTrim(i)
        SLID = log_ScrapLog(_MMTID=i,_VID=1)
        # Log Scrap has begun , Need aspect to identify Scrap complete at end? EndDt Update?
        url_1st = Url_Multi(make=_make, model=_model, trim=_trim, pgsize=100)
        IDs, NumEntry = Scrap_IDs(url_1st)
        

def Loop_ManyIDs():
    MMT_All = get_MMTrim(_MMTID=0)
    for i in MMT_All.MMTID.values:
        Vehicle = get_VINs(_MMTID = i)
        for v in range(Vehicle.shape[0]):
            Vehicle[v]

            sleep(5)
            Url_Single()



#Wrap in loop to run till out of pages - identify how many pages, by scrapping on page 1 # available
# Get url for select car types
Url_Multi(page=5,pgsize=50,make='toyota',model='toyota-camry',trim='toyota-camry-se',yrmin='2018',yrmax='2018',mile='',type='used',sort='list_price',maxdist='all',zip='57193')
# Scrap the URL for multiple IDs
cars_url = 'https://www.cars.com/shopping/results/?page=2&page_size=20&dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=toyota&maximum_distance=all&mileage_max=&models[]=toyota-camry&sort=best_match_desc&stock_type=used&trims[]=toyota-camry-se&year_max=2018&year_min=2018&zip=57193'
Scrap_IDs(cars_url)
# Log into Meta with VID #1 (Default Non-Car)
SMID = log_ScrapMeta(1,'CDCID', 'b2387cb6-7a74-4608-add3-274f4e578576' )

# Check to see if new car scrapped and log into vehicles
VID = log_Vehicle(_VIN = 'ASDLFK234234SF', _MMID = 0, _CDCID = 'b2387cb6-7a74-4608-add3-274f4e578576' )




