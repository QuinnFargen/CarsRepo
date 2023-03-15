# CarsRepo

[Cars.com](https://www.cars.com/ "Cars.com Homepage")

<img src="https://github.com/QuinnFargen/CarsRepo/blob/main/MakesModels/CarsDotComLogo.png" data-canonical-src="https://github.com/QuinnFargen/CarsRepo/blob/main/MakesModels/CarsDotComLogo.png" width="300" height="155" />

[Edmunds.com](https://www.edmunds.com/ "Edmunds Homepage")

<img src="https://github.com/QuinnFargen/CarsRepo/blob/main/MakesModels/EdmundsLogo.png" data-canonical-src="https://github.com/QuinnFargen/CarsRepo/blob/main/MakesModels/EdmundsLogo.png" width="300" height="155" />


## Objective
Curently using Cars.com (CDC) & Edmunds to scrap popular makes and models to collect what is listed. 
Python process to loop through stored makes and models in sqlite DB and log back scraped values into DB.
Want to make maintainable to see a car listed, sold and re-listed later to see change over time by VIN.
Ultimately want to practice python scraping, DB design, dashboard summary on captured data.

## Capabilities
Previously built a brute force method to loop thru pages gathering posting, then looped thru postings (Not human behavior like).
Capable of being blocked by Cars.com :), so working to be polite and shifty.
Currently refactoring into classes as well as a new method of going to each posting right away and back to the multiple listing page (Human like).

## Table of Contents:
### [CarsWebsite](https://github.com/QuinnFargen/CarsRepo/blob/main/Scraper/CarsWebsite.py)
When passing Car Type or VIN, returns url as well as parsing requested pages.
### [CarsDB](https://github.com/QuinnFargen/CarsRepo/blob/main/Storage/CarsDB.py)
Connect to sqlite DB, Query & Insert functions
### [CarsScrap](https://github.com/QuinnFargen/CarsRepo/blob/main/Scraper/CarsScrap.py)
Requesting url with ScraperAPI or manual method of rotating header.
### [CarsWalker](https://github.com/QuinnFargen/CarsRepo/blob/main/Scraper/CarsWalker.py)
New method of walking multiple listing page more human like.
### [CarsLoop](https://github.com/QuinnFargen/CarsRepo/blob/main/Scraper/CarsLoop.py)
Old method to loop through pages to scrap IDs, and loop known IDs to refresh/check.


## Future Goals
+ Refactor to crawl individual url meta from multi listing page (more human like).
+ Move to online database from sqlite local
+ Grab url to photo of vehicle
+ Practice setting up on Azure
+ Host dashboard on [QuinnFargen.com](https://quinnfargen.com/)
+ Extend to other car listing websites