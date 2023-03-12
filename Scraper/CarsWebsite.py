

class Website():

    def __init__(self,_Url_Multi,_Url_Single,_Scrap_Car,_Scrap_IDs):
        self.Url_Multi = _Url_Multi
        self.Url_Single = _Url_Single
        self.Scrap_Car = _Scrap_Car
        self.Scrap_IDs = _Scrap_IDs

    def get_allLinks(self, CarsURL):
        IDs = self.Scrap_IDs(CarsURL)
        Urls = []
        for i in range(len(IDs)):
            Urls.append(self.Url_Single(_allfour = IDs[i]))
        return Urls
    
 


# from Edmund.EdmParse import Scrap_Car, Scrap_IDs
# from Edmund.EdmURL import Url_Multi, Url_Single

# Edmund = Website(_Url_Multi=Url_Multi, _Url_Single=Url_Single, _Scrap_Car=Scrap_Car, _Scrap_IDs=Scrap_IDs)

# Url = 'https://www.edmunds.com/inventory/srp.html?inventorytype=used%2Ccpo&make=honda&model=civic&radius=6000'

# Edmund.get_allLinks(Url)

