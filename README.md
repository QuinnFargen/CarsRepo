# CarsRepo

[Cars.com](https://www.cars.com/ "Cars.com Homepage")
![logo](https://github.com/QuinnFargen/CarsRepo/blob/main/MakesModels/CarsDotComLogo.png )



## Objective
Curently using Cars.com (CDC) to scrap popular makes and models to collect what is listed. 
Python process to loop through stored makes and models in sqlite DB and log back scraped values into DB.
Want to make maintainable to see a car listed, sold and re-listed later to see change over time by VIN.
Ultimately want to practice python scraping, DB design, dashboard summary on captured data.

## Capabilities
Currently 2 different loops with one to acquire listed url's and another to go to each listing to get additional meta data.
Capable of being blocked by Cars.com :), so working to be polite and shifty.

## Table of Contents:
### CarsURL
When passing Car Type or VIN, returns Cars.com url
### CarsDB
Connect to sqlite DB, Query & Insert functions
### CarsScrap
Requesting url with ScraperAPI or manual method of rotating header.
### CarsParse
With scraped website, clean and parse to values wanted
### CarsLoop
Loops through pages to scrap IDs, and loop known IDs to refresh/check.


## Future Goals
+ Refactor to crawl individual url meta from multi listing page (more human like).
+ Move to online database from sqlite local
+ Practice setting up on Azure
+ Host dashboard on [QuinnFargen.com](https://quinnfargen.com/)
+ Extend to other websites