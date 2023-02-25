
import sqlite3
import pandas as pd
from datetime import datetime

########################################################
# DB Connections & Cursors

def get_CDC_ConCur():
    con = sqlite3.connect("CDC.db")
    cur = con.cursor()
    return con, cur

########################################################
# Query from sql what cars we want to scrap

def get_MMTrim(_MMTID = 0,_NonTrim=0):
    """
    Get MMTrim all Columns with additional, MMTID optional WHERE.
    :param _MMTID(0)
    :return MMT(pd),_make,_model,_trim,_minYr,_maxYr
    """
    con, cur = get_CDC_ConCur()
    where = ""
    if _MMTID != 0:
        where = " WHERE M.MMTID = " + str(_MMTID)
        query = "SELECT * from MMTrim m" + where
    else:
        query = "SELECT * from MakeModel m" + where
    MMT = pd.read_sql_query(query, con)
    _make = MMT["CDCmake"].values[0]
    _model = MMT["CDCmodel"].values[0]
    _trim = MMT["CDCtrim"].values[0]
    _minYr = MMT["minYr"].values[0]
    _maxYr = MMT["maxYr"].values[0]
    if _maxYr is None:
        _maxYr = datetime.now().year
    if _MMTID == 0:
        return MMT
    return MMT, _make, _model, _trim, _minYr, _maxYr

def get_ScrapLog_SLID(_MMTID = 0):
    """
    Get ScrapLog all Columns, MMTID optional WHERE.
    :param _MMTID(0)
    :ScrapLog(pd)
    """
    con, cur = get_CDC_ConCur()
    where = " WHERE S.IDsDoneDt IS NULL"
    if _MMTID != 0:
        where += " AND S.MMTID = " + str(_MMTID)
    query = "SELECT * from ScrapLog S" + where
    ScrapLog = pd.read_sql_query(query, con)
    return ScrapLog

def get_Meta_SLIDTagname(_SLID=0,_TagName=''):
    """
    Get ScrapMeta (SMID, TagValue & InsertDate), WHERE Not Optional.
    :param _SLID(0),_TagName('')
    :ScrapMeta(pd)
    """
    con, cur = get_CDC_ConCur()
    if _SLID != 0 and _TagName != '':
        where = " WHERE S.SLID = " + str(_SLID) + " AND S.TagName = '" + _TagName + "'"
        query = "SELECT S.SMID, S.TagValue, S.InsertDate from ScrapMeta S" + where
        ScrapMeta = pd.read_sql_query(query, con)
        return ScrapMeta


def get_Vehicle_VinCdcID(_VIN='',_CDCID='',_VinNULL=0):
    con, cur = get_CDC_ConCur()
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
    Vehicle = pd.read_sql_query(query, con)
    return Vehicle



########################################################
# Insert into sql results of scrapping

def log_ScrapLog(_MMTID = 0, _VID = 1, _SLID = 0, _IDsDone=0):
    """
    Log a new Scrap. 
    :param _MMTID(0), _VID(1), _SLID(0)
    :return SLID
    """
    con, cur = get_CDC_ConCur()
    if _SLID != 0 and _IDsDone == 0:
        updt = "UPDATE ScrapLog SET LogDoneDt = DATETIME() WHERE SLID = " + str(_SLID)
        cur.execute(updt)
        con.commit(); con.close()
        return
    if _SLID != 0 and _IDsDone == 1:
        updt = "UPDATE ScrapLog SET IDsDoneDt = DATETIME(), LogDoneDt = DATETIME() WHERE SLID = " + str(_SLID)
        cur.execute(updt)
        con.commit(); con.close()
        return
    cur.execute('''INSERT INTO ScrapLog (MMTID,VID) VALUES (?, ?)''',(_MMTID,_VID))
    SLID = cur.lastrowid
    con.commit(); con.close()
    return SLID


def log_ScrapMeta(_VID = 1, _TagName = '', _TagValue = '', _SLID = 0, _WantSMID = 0):
    """
    Log new Scrap Meta
    :params VID TagName TagValue:
    :return: SMID
    """
    con, cur = get_CDC_ConCur()
    cur.execute('''INSERT INTO ScrapMeta (VID,TagName,TagValue,SLID) VALUES (?,?,?,?)''',(_VID,_TagName,_TagValue,_SLID))
    SMID = cur.lastrowid
    con.commit(); con.close()
    if _WantSMID == 1:
        return SMID

def log_Vehicle(_IsUpdate=0,_VIN='',_MMTID='',_CDCID='',_LastScrapDt='',_IsActive=1,_RetVID=0):
    """
    Log a new Vehicle, or Update LastScrapDt/IsActive/VIN/MMTID
    :param _CDCID:
    :param OPTIONAL: _IsUpdate,_VIN,_MMTID,_LastScrapDt,_IsActive,_RetVID
    :return: VID
    """
    con, cur = get_CDC_ConCur()
    if _IsUpdate == 0:              # Only Non-Update is new Update CDCID
        cur.execute('''INSERT INTO Vehicle (CDCID,MMTID,LastScrapDt) VALUES (?,?,?)''', (_CDCID,_MMTID,_LastScrapDt) )    
    elif _IsActive == 0:            # Update No Longer Active Vehicle        
        cur.execute(  ''' UPDATE Vehicle SET IsActive = 0, LastScrapDt = ? WHERE CDCID = ? ''', (_LastScrapDt,_CDCID) )                                          
    elif _LastScrapDt != '':        # Update newest ScrapDt
        cur.execute(  ''' UPDATE Vehicle SET LastScrapDt = ? WHERE CDCID = ? ''', (_LastScrapDt,_CDCID) )   
    elif _VIN != '':
        cur.execute(  ''' UPDATE Vehicle SET VIN = ? WHERE CDCID = ? ''', (_VIN,_CDCID) )   
    elif _MMTID != '':
        cur.execute(  ''' UPDATE Vehicle SET MMTID = ? WHERE CDCID = ? ''', (_MMTID,_CDCID) )           
    VID = cur.lastrowid
    con.commit(); con.close()
    if _RetVID ==1:
        return VID



