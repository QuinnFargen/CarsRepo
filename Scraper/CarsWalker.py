
from Storage.CarsDB import CarsRepoDB
from Scraper.CarsWebsite import Website
from Scraper.CarsScrap import Scrap


class CarZombie(CarsRepoDB, Website, Scrap):

    def __init__(self):
        CarsRepoDB.__init__(self)
        Website.__init__(self)

    def get_allLinks(self, CarsURL):
        Scrap = self.Scrap_IDs(CarsURL)
        Urls = []; IDs = Scrap[0]
        for i in range(len(IDs)):
            Urls.append(self.Url_Single(IDs[i]))
        return Urls

    def get_pop(self, _MMTID=''):
        MMT_All = self.get_MMTrim(_MMTID=_MMTID) 
        print(MMT_All)



    

Brains = CarZombie()

Brains.get_pop()





