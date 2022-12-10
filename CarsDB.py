
import sqlite3
import pandas as pd


########################################################
# DB Connections & Cursors

def get_CDC_con():
    con = sqlite3.connect("CDC.db")
    return con

def get_CDC_cur():
    con = get_CDC_con()
    cur = con.cursor()
    return cur


########################################################
# Query from sql what cars we want to scrap

def get_MMTrim(MMID = 0):
    con = get_CDC_con()
    where = ""
    if MMID != 0:
        where = " WHERE M.MMID = " + str(MMID)
    query = "SELECT * from MMTrim m" + where
    return pd.read_sql_query(query, con)

# df2 = get_CarsToScrap(1)
# print(df2.head())


# Insert into sql results of scrapping

def log_ScrapLog(MMID = 0, VID = 1):
    con = get_CDC_con()
    cur = get_CDC_cur()
    query ='''INSERT INTO ScrapLog (MMID, VID)  
            VALUES (''' + str(MMID) + ',' + str(VID) + ');'
    cur.execute(query)
    con.commit()
    return cur.lastrowid

SLID = log_ScrapLog(1,1)

cur.execute("""
INSERT INTO MMTrim (MMID, CDCmake, CDCmodel, CDCtrim)
SELECT ('1','toyota','toyota-camry','toyota-camry-se');
""")
con.commit()


df = pd.read_sql_query("SELECT * from ScrapLog", con)

# Verify that result of SQL query is stored in the dataframe

print(df.head())

con.close()