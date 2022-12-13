

from CarsURL import Url_Multi, Url_Single
from CarsScrap import Scrap_IDs, Scrap_Car
from CarsDB import log_ScrapLog, log_ScrapMeta, log_Vehicle, get_MMTrim



#Query aspects to scrap
MMT = get_MMTrim()

# Log Scrap has begun , Need aspect to identify Scrap complete at end? EndDt Update?
SLID = log_ScrapLog(1,1)

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



