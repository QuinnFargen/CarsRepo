
from CarsURL import Url_Multi, Url_Single
from CarsScrap import Scrap_IDs, Scrap_Car
from CarsDB import log_ScrapLog

SLID = log_ScrapLog(1,1)



Url_Multi(page=5,pgsize=50,make='toyota',model='toyota-camry',trim='toyota-camry-se',yrmin='2018',yrmax='2018',mile='',type='used',sort='list_price',maxdist='all',zip='57193')
Url_Single('6313112d-5f5e-4b8e-b751-57bfcd331f96')



