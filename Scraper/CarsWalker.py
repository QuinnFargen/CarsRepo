
from Storage.CarsDB import CarsRepoDB
from CarsWebsite import Edmund, CarsCom


class CarZombie(CarsRepoDB,Edmund, CarsCom):

    def __init__(self):
        CarsRepoDB.__init__(self)
        Edmund.__init__(self)
        CarsCom.__init__(self)






    







