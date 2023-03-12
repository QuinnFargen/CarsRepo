
from Storage.CarsDB import CarsRepoDB
from Scraper.CarsWebsite import Website
from Scraper.CarsScrap import Scrap


class CarZombie(CarsRepoDB, Website, Scrap):

    def __init__(self,Domain):
        CarsRepoDB.__init__(self)
        Website.__init__(self,Domain)
        Scrap.__init__(self)

    def get_allLinks(self, CarsURL):
        soup = self.get_soup(CarsURL,'spicy')
        Scrap = self.Scrap_IDs(soup)
        Urls = []; IDs = Scrap[0]
        for i in range(len(IDs)):
            Urls.append(self.Url_Single(IDs[i]))
        return Urls

    def get_pop(self, MMTID=0):
        MMT_All = self.get_MMTrim(_MMTID=MMTID) 
        print(MMT_All)



    

Brains = CarZombie('CDC')
Brains.get_pop(MMTID=0)






