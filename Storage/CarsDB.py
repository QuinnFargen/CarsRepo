
import sqlite3
import pandas as pd
from datetime import datetime
import os



class CarsRepoDB():

    def __init__(self):
        self.con = self.get_CDC_ConCur(ConCur='con')
        self.cur = self.get_CDC_ConCur(ConCur='cur')


    ########################################################
    # DB Connections & Cursors

    def get_CDC_ConCur(self, ConCur):
        os.chdir('/Users/quinnfargen/Documents/GitHub/CarsRepo/Storage')
        con = sqlite3.connect("CarsRepo.db")
        cur = con.cursor()
        if ConCur == 'con':
            return con
        return cur
    
    ########################################################
    # Query from sql what cars we want to scrap

    def get_MMT(self,_MMTID = 0,_NonTrim=0):
        """
        Get MMTrim all Columns with additional, MMTID optional WHERE.
        :param _MMTID(0)
        :return MMT(pd),_make,_model,_trim,_minYr,_maxYr
        """
        where = ""
        if _MMTID != 0:
            where = " WHERE m.MMTID = " + str(_MMTID)
            query = "SELECT * from MMT m" + where
        elif _NonTrim == 1:
            query = "SELECT * FROM MakeModel m"
        else:
            query = "SELECT * from MMT m" + where
        MMT = pd.read_sql_query(query, self.con)
        return MMT 

    def get_ScrapLog_SLID(self,_MMTID = 0):
        """
        Get ScrapLog all Columns, MMTID optional WHERE.
        :param _MMTID(0)
        :ScrapLog(pd)
        """
        where = " WHERE S.IDsDoneDt IS NULL"
        if _MMTID != 0:
            where += " AND S.MMTID = " + str(_MMTID)
        query = "SELECT * from ScrapLog S" + where
        ScrapLog = pd.read_sql_query(query, self.con)
        return ScrapLog

    def get_Meta_SLIDTagname(self,_SLID=0,_TagName=''):
        """
        Get ScrapMeta (SMID, TagValue & InsertDate), WHERE Not Optional.
        :param _SLID(0),_TagName('')
        :ScrapMeta(pd)
        """
        if _SLID != 0 and _TagName != '':
            where = " WHERE S.SLID = " + str(_SLID) + " AND S.TagName = '" + _TagName + "'"
            query = "SELECT S.SMID, S.TagValue, S.InsertDate from ScrapMeta S" + where
            ScrapMeta = pd.read_sql_query(query, self.con)
            return ScrapMeta

    def get_Vehicle_VinCdcID(self,_VIN='',_CDCID='',_VinNULL=0):
        where = ''
        if _VinNULL == 1:
            where += "v.VIN IS NULL"
        elif _VIN == '' and _CDCID == '':
            return
        elif _VIN != '':
            where += "v.VIN = '" + _VIN + "'"
        elif _CDCID != '':
            where += "v.CDCID = '" + _CDCID + "'"
        query = "SELECT * from Vehicle v WHERE " + where
        Vehicle = pd.read_sql_query(query, self.con)
        return Vehicle



    ########################################################
    # Insert into sql results of scrapping

    def log_ScrapLog(self,_MMTID = 0, _VID = 1, _SLID = 0, _IDsDone=0):
        """
        Log a new Scrap. 
        :param _MMTID(0), _VID(1), _SLID(0)
        :return SLID
        """
        if _SLID != 0 and _IDsDone == 0:
            updt = "UPDATE ScrapLog SET LogDoneDt = DATETIME() WHERE SLID = " + str(_SLID)
            self.cur.execute(updt)
            self.con.commit(); self.con.close()
            return
        if _SLID != 0 and _IDsDone == 1:
            updt = "UPDATE ScrapLog SET IDsDoneDt = DATETIME(), LogDoneDt = DATETIME() WHERE SLID = " + str(_SLID)
            self.cur.execute(updt)
            self.con.commit(); self.con.close()
            return
        self.cur.execute('''INSERT INTO ScrapLog (MMTID,VID) VALUES (?, ?)''',(_MMTID,_VID))
        SLID = self.cur.lastrowid
        self.con.commit(); self.con.close()
        return SLID

    def log_ScrapMeta(self,_VID = 1,_TagName = '',_TagValue = '',_SLID = 0,_WantSMID = 0):
        """
        Log new Scrap Meta
        :params VID TagName TagValue:
        :return: SMID
        """
        self.cur.execute('''INSERT INTO ScrapMeta (VID,TagName,TagValue,SLID) VALUES (?,?,?,?)''',(_VID,_TagName,_TagValue,_SLID))
        SMID = self.cur.lastrowid
        self.con.commit(); self.con.close()
        if _WantSMID == 1:
            return SMID

    def log_Vehicle(self,_IsUpdate=0,_VIN='',_MMTID='',_CDCID='',_LastScrapDt='',_IsActive=1,_RetVID=0):
        """
        Log a new Vehicle, or Update LastScrapDt/IsActive/VIN/MMTID
        :param _CDCID:
        :param OPTIONAL: _IsUpdate,_VIN,_MMTID,_LastScrapDt,_IsActive,_RetVID
        :return: VID
        """
        if _IsUpdate == 0:              # Only Non-Update is new Update CDCID
            self.cur.execute('''INSERT INTO Vehicle (CDCID,MMTID,LastScrapDt) VALUES (?,?,?)''', (_CDCID,_MMTID,_LastScrapDt) )    
        elif _IsActive == 0:            # Update No Longer Active Vehicle        
            self.cur.execute(  ''' UPDATE Vehicle SET IsActive = 0, LastScrapDt = ? WHERE CDCID = ? ''', (_LastScrapDt,_CDCID) )                                          
        elif _LastScrapDt != '':        # Update newest ScrapDt
            self.cur.execute(  ''' UPDATE Vehicle SET LastScrapDt = ? WHERE CDCID = ? ''', (_LastScrapDt,_CDCID) )   
        elif _VIN != '':
            self.cur.execute(  ''' UPDATE Vehicle SET VIN = ? WHERE CDCID = ? ''', (_VIN,_CDCID) )   
        elif _MMTID != '':
            self.cur.execute(  ''' UPDATE Vehicle SET MMTID = ? WHERE CDCID = ? ''', (_MMTID,_CDCID) )           
        VID = self.cur.lastrowid
        self.con.commit(); self.con.close()
        if _RetVID ==1:
            return VID



