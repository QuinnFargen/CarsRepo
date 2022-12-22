

from CarsURL import Url_Multi, Url_Single
from CarsScrap import Scrap_IDs, Scrap_Car

from CarsDB import log_ScrapLog, log_ScrapMeta, log_Vehicle, get_MMTrim, get_VINs
from time import sleep



def Loop_ManyMulti(_MMTID = 0,_pgsize = 100):
    MMT_All = get_MMTrim(_MMTID=_MMTID)                 # Gets All MMTID if ZERO
    for i in range(MMT_All.shape[0]):
        MMTID = MMT_All.loc[i]['MMTID']        
        MMT, make, model, trim = get_MMTrim(MMTID)
        SLID = log_ScrapLog(_MMTID=MMTID,_VID=1)
        url_1st = Url_Multi(_make=make, _model=model, _trim=trim, _pgsize=_pgsize, _yrmax = '2018', _yrmin = '2018')
        IDs, NumEntry = Scrap_IDs(url_1st)
        log_ScrapMeta(_VID = 1, _TagName = 'NumEntry'  , _TagValue = str(NumEntry), _SLID = SLID)    
        for n in range(round(NumEntry / _pgsize) + 1):  # Loop Thru # Entry Available / # on Pg          
            sleep(5)                                    # Don't bombard them :)
            url_n = Url_Multi(_page=n+1, _make=make, _model=model, _trim=trim, _pgsize=_pgsize, _yrmax = '2018', _yrmin = '2018')
            log_ScrapMeta(_VID = 1, _TagName = 'url_' + str(n)  , _TagValue = url_n, _SLID = SLID)   
            IDs, NumEntry = Scrap_IDs(url_n)  
            for d in range(len(IDs)):                   # Loop Thru, Log each ID Scrapped
                log_ScrapMeta(_VID = 1, _TagName = 'CDCID', _TagValue = IDs[d], _SLID = SLID)       
        #Finish the Scarp & Update the LogDoneDt    
        log_ScrapLog(_SLID = SLID)
           
        

def Loop_ManyIDs_ToVIN():
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




