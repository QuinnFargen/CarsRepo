
import sqlite3
import pandas as pd



########################################################
# DB Connections & Cursors

def get_CDC_ConCur():
    con = sqlite3.connect("CDC.db")
    cur = con.cursor()
    return con, cur

########################################################
# Query from sql what cars we want to scrap

def get_MMTrim(_MMTID = 0):
    con, cur = get_CDC_ConCur()
    where = ""
    if _MMTID != 0:
        where = " WHERE M.MMTID = " + str(_MMTID)
    query = "SELECT * from MMTrim m" + where
    return pd.read_sql_query(query, con)


########################################################
# Insert into sql results of scrapping

def log_ScrapLog(_MMTID = 0, _VID = 1):
    """
    Log a new Scrap
    :param MMTID:
    :param VID:
    :return: SLID
    """
    con, cur = get_CDC_ConCur()
    cur.execute('''INSERT INTO ScrapLog (MMTID,VID) VALUES (?, ?)''',(_MMTID,_VID))
    SLID = cur.lastrowid
    con.commit(); con.close()
    return SLID

def log_ScrapMeta(_VID = 1, _TagName = '', _TagValue = '', _SLID = 0):
    """
    Log new Scrap Meta
    :param VID:
    :param TagName:
    :param TagValue:
    :return: SMID
    """
    con, cur = get_CDC_ConCur()
    cur.execute('''INSERT INTO ScrapMeta (VID,TagName,TagValue,SLID) VALUES (?,?,?,?)''',(_VID,_TagName,_TagValue,_SLID))
    SMID = cur.lastrowid
    con.commit(); con.close()
    return SMID

def log_Vehicle(_VIN = '', _MMTID = 0, _CDCID = '', _FirstDt = ''):
    """
    Log a new Vehicle
    :param VIN:
    :param MMTID:
    :param FirstDt: OPTIONAL
    :param CDCID:
    :return: VID
    """
    con, cur = get_CDC_ConCur()
    if _FirstDt != '':  # Insert FirstDt if given
        cur.execute('''INSERT INTO Vehicle (VIN,MMTID,FirstDt,CDCID) VALUES (?, ?, ?, ?)''', (_VIN,_MMTID,_FirstDt,_CDCID) )
    else:               # Else let default getdate()
        cur.execute('''INSERT INTO Vehicle (VIN,MMTID,CDCID) VALUES (?, ?, ?)''', (_VIN,_MMTID,_CDCID) )        
    VID = cur.lastrowid
    con.commit(); con.close()
    return VID



# SLID = log_ScrapLog(1,1)
# SLID = log_ScrapMeta(1,'CDCID', 'b2387cb6-7a74-4608-add3-274f4e578576' )
# SLID = log_Vehicle(_VIN = 'ASDLFK234234SF', _MMID = 0, _CDCID = 'b2387cb6-7a74-4608-add3-274f4e578576' )

# con, cur = get_CDC_ConCur()
# print(pd.read_sql_query("SELECT * from ScrapLog", con))
# print(pd.read_sql_query("SELECT * from ScrapMeta", con))
# print(pd.read_sql_query("SELECT * from Vehicle", con))

    #Querying multiple columns
# res = new_cur.execute("SELECT title, year FROM movie ORDER BY score DESC")
# title, year = res.fetchone()



# df2 = get_MMTrim(1); print(df2.head())

# df = pd.read_sql_query("SELECT * from ScrapLog", con)

# # Verify that result of SQL query is stored in the dataframe

# print(df.head())

# con.close()