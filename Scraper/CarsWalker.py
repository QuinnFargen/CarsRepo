
from Storage.CarsDB import CarsRepoDB
from Scraper.CarsWebsite import Website
from Scraper.CarsScrap import Scrap

class CarZombie(CarsRepoDB, Website, Scrap):

    def __init__(self, Domain):
        CarsRepoDB.__init__(self)
        Website.__init__(self,Domain)
        Scrap.__init__(self,Domain)
        self.MMTID = 1
        self.NonTrim = 0
        self.MMT = self.get_MMT(_MMTID=self.MMTID,_NonTrim=self.NonTrim) 
        self.MMTnum = 0
        self.MMTcur = self.MMT.iloc[self.MMTnum, :].tolist()
        self.pgnum = 0
        self.numEntry = 0
        self.MultiUrl = self.get_MultiUrl()
        self.URls = self.get_allLinks()

    def get_MultiUrl(self):
        # 0:MMID, 1:MMTID, 2:make, 3:model, 4:trim, 5:minYr, 6:maxYr
        return self.Url_Multi(_page=self.pgnum,_make=self.MMTcur[2],_model=self.MMTcur[3],_trim=self.MMTcur[4],_yrmin=self.MMTcur[5],_yrmax=self.MMTcur[6])
         
    def get_allLinks(self):
        soup = self.get_soup(self.MultiUrl,'spicy')
        Scrap = self.Scrap_IDs(soup)
        Urls = []; IDs = Scrap[0]
        self.numEntry = Scrap[1]
        for i in range(len(IDs)):
            Urls.append(self.Url_Single(IDs[i]))
        return Urls
    
    def stagger(self):
        self.SLID = self.log_ScrapLog(_MMTID=self.MMTID,_VID=1)
        for s in range(self.numEntry / 100):
            for u in range(len(self.URls)):
                pass
            self.pgnum += 1
            self.MultiUrl = self.get_MultiUrl()
        self.log_ScrapLog(_SLID = self.SLID)






    

Brains = CarZombie('CDC')
Brains.MultiUrl
Brains.URls
Brains.numEntry
Brains.MMT
Brains.MMTcur


DB = CarsRepoDB()
mmtTest = DB.get_MMT(_NonTrim=1)
mmtTest.iloc[0].tolist()

Web = Website(Domain='CDC')
Web.Url_Multi(_page=0,_make='toyota',_model='camry')

params = ['https://www.cars.com/shopping/results/?','','makes[]=toyota']
Web.paramComb(pars=params)