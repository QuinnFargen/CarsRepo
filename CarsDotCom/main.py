
#############################################################################################
## Two Aproaches:


#############################################################################################
## 1 - Loop thru all, then go back and get Additional Meta individual calls

from CarsLoop import Loop_MMTID_GetCDCID, Loop_SLID_ToVID

# Go looking for new Listings:
Loop_MMTID_GetCDCID()  
# Clean up new data
Loop_SLID_ToVID()
# Make individual calls update listings/check still exist


#############################################################################################
## 2 - Loop thru all and make individual calls as you go along. can pass url




# https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/
# https://brightdata.com/blog/how-tos/user-agents-for-web-scraping-101
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referer


