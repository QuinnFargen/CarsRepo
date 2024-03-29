

from CarsDotCom.CDCURL import Url_Multi, Url_Single
from CarsDotCom.CDCParse import Scrap_IDs, Scrap_Car
from Storage.CarsRepoDB import log_ScrapLog, log_ScrapMeta, log_Vehicle, get_MMTrim, get_Vehicle_VinCdcID, get_ScrapLog_SLID, get_Meta_SLIDTagname
from time import sleep


def Loop_MMTID_GetCDCID(_MMTID=0,_OnlyMM=0,_pgsize=100):
    """
    Loop thru passed MMTID or all active, log CDCIDs for active listings
    Param:  _MMTID (Def=0), _pgsize (Def=100)
    Return: None
    """
    MMT_All = get_MMTrim(_MMTID=_MMTID)                     # Gets All MMTID if ZERO
    for m in range(MMT_All.shape[0]):
        MMTID = int(MMT_All.loc[m]['MMTID'])
        MMT, make, model, trim, minyr, maxyr = get_MMTrim(MMTID)
        SLID = log_ScrapLog(_MMTID=MMTID,_VID=1)            #Log Start of scrap, get SLID to tie other logs with
        yrs = check_None_minyr(_minyr=minyr, _maxyr=maxyr)  #Check if Year min/max exist, if not just loop once
        for y in range(len(yrs)):
            yr = str(yrs[y])
            url_1st = Url_Multi(_make=make, _model=model, _trim=trim, _pgsize=_pgsize, _yrmax = yr, _yrmin = yr)
            IDs, NumEntry = Scrap_IDs(url_1st)
            log_ScrapMeta(_VID = 1, _TagName = 'Num_Yr_' + yr  , _TagValue = str(NumEntry), _SLID = SLID)    
            for n in range(round(NumEntry / _pgsize) + 1):  # Loop Thru # Entry Available / # on Pg          
                sleep(5)                                    # Don't bombard them :)
                url_n = Url_Multi(_page=n+1, _make=make, _model=model, _trim=trim, _pgsize=_pgsize, _yrmax = yr, _yrmin = yr)
                log_ScrapMeta(_VID = 1, _TagName = 'url_Yr_' + yr + '_' + str(n)  , _TagValue = url_n, _SLID = SLID)   
                IDs, NumEntry = Scrap_IDs(url_n)  
                for d in range(len(IDs)):                   # Loop Thru, Log each ID Scrapped
                    log_ScrapMeta(_VID = 1, _TagName = 'CDCID', _TagValue = IDs[d], _SLID = SLID)       
        #Finish the Scarp & Update the LogDoneDt    
        log_ScrapLog(_SLID = SLID)
           

# Go thru new Meta CDCIDs, add to Vehicle table       
def Loop_SLID_ToVID():
    """
    Loop thru SLID of new CDCID's that need to be added to Vehicle
    Param:  None
    Return: None
    """
    NeedIDd = get_ScrapLog_SLID()
    for n in range(NeedIDd.shape[0]):
        SLID = NeedIDd["SLID"].values[n]
        MMTID = str(NeedIDd["MMTID"].values[n])
        Meta = get_Meta_SLIDTagname(SLID, 'CDCID')
        for m in range(Meta.shape[0]):
            #Check if exists, if then log updateDate
            CDCID = Meta["TagValue"].values[m]
            LastScrapDt = Meta["InsertDate"].values[m]
            Vehicle = get_Vehicle_VinCdcID(_CDCID=CDCID)
            if Vehicle.shape[0] != 0:
                log_Vehicle(_IsUpdate=1,_CDCID=CDCID,_LastScrapDt=LastScrapDt)
            else:       #Else insert new to Vehicle
                log_Vehicle(_CDCID=CDCID,_MMTID=MMTID,_LastScrapDt=LastScrapDt)
        # Update done
        log_ScrapLog(_SLID=SLID,_IDsDone=1)


def Loop_Vehicle_AddVIN():
    """
    Loop thru Vehicle that need VIN, ind url call meta data logged.
    Param:  None
    Return: None
    """
    NeedVIN = get_Vehicle_VinCdcID(_VinNULL=1)
    for v in range(NeedVIN.shape[0]):
        sleep(3)    #Be Nice to CDC
        CDCID = NeedVIN["CDCID"].values[v]
        VID = str(NeedVIN["VID"].values[v])
        MMTID = str(NeedVIN["MMTID"].values[v])
        SLID = log_ScrapLog(_MMTID=MMTID,_VID=VID)            #Log Start of scrap, get SLID to tie other logs with
        url = Url_Single(CDCID)
        attr = Scrap_Car(url)  
        print(url); print(attr)   
        if attr == {'Status': 'No Longer'}:
            log_Vehicle(_CDCID=CDCID,_IsActive=0,_IsUpdate=1)
        for a in sorted(attr):
            log_ScrapMeta(_VID = VID, _SLID = SLID, _TagName = a, _TagValue = attr[a])   
            if a == 'VIN':
                log_Vehicle(_IsUpdate=1,_CDCID=CDCID,_VIN=attr[a])
        #Update VID with VIN Scrapped
        log_ScrapLog(_SLID = SLID,_IDsDone=1)                          #Finish the Scarp & Update the LogDoneDt    


# Go thru new VIN Meta & Create new MMTID, UPDATE MMTID of VIN






##############################################
## Suplemental functions

def check_None_minyr(_minyr=0,_maxyr=0):
    if _minyr is None:
        return range(0,1)
    else:
        return range(_minyr,_maxyr)






# #Wrap in loop to run till out of pages - identify how many pages, by scrapping on page 1 # available
# # Get url for select car types
# Url_Multi(page=5,pgsize=50,make='toyota',model='toyota-camry',trim='toyota-camry-se',yrmin='2018',yrmax='2018',mile='',type='used',sort='list_price',maxdist='all',zip='57193')
# # Scrap the URL for multiple IDs
# cars_url = 'https://www.cars.com/shopping/results/?page=2&page_size=20&dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=toyota&maximum_distance=all&mileage_max=&models[]=toyota-camry&sort=best_match_desc&stock_type=used&trims[]=toyota-camry-se&year_max=2018&year_min=2018&zip=57193'
# Scrap_IDs(cars_url)
# # Log into Meta with VID #1 (Default Non-Car)
# SMID = log_ScrapMeta(1,'CDCID', 'b2387cb6-7a74-4608-add3-274f4e578576' )

# # Check to see if new car scrapped and log into vehicles
# VID = log_Vehicle(_VIN = 'ASDLFK234234SF', _MMID = 0, _CDCID = 'b2387cb6-7a74-4608-add3-274f4e578576' )




