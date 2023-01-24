

from CarsLoop import Loop_MMTID_GetCDCID, Loop_SLID_ToVID


# Go looking for new Listings:
Loop_MMTID_GetCDCID()  
# Clean up new data
Loop_SLID_ToVID()
# Make individual calls update listings/check still exist




# Table of Contents:
#   CarsURL
#       When passing Car Type or VIN, returns Cars.com url
#   CarsDB
#       Connect to sqlite DB, Query & Insert functions
#   CarsScrp
#       Requesting url, Scrapping & cleaning to values wanted
#   CarsLoop
#       Loops through pages to scrap IDs, and loop known IDs to refresh/check.







