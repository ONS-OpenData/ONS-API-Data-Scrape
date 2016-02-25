# ONS-API-Data-Scrape
A json file (and the script to create it) containing context, name, dimensions and dimension items for all datasets available via the ONS API service.

----

NOTE - the webscrape on this page only deals with the Economic and Social datasets. I will be adding the Census datasets in the next few days (written 25/2/2015) as  it'll take a while to scrape given the amount of data involved.

About
This repo is for a web scraping script and resulting JSON file of the open data content availible from the Office for National Statistics via the API.
The idea here is to allow non developers to explore the content on the API without having to wade through code documentation (i.e worry about the how you're going to retrieve the data AFTER you've identified something you need).
The scrape is downloadable as a tiered JSON file. Structure wise, it looks like this:
 
How do I use the Scraper?
in most cases it's far easier to just download the JSON file on this page. However should you wish to create your own scrape (to get your API key into the urls for example), then navigate to the directory you've downloaded it and the API tools script and use:
python WDA_Scraper.py "APIkey"
With "APIkey2 being the one you are assigned after signing up to the openAPI BETA - https://www.ons.gov.uk/ons/apiservice/web/apiservice/home

How do I use this JSON file?
Download WDA_Scrape.json to your PC (or use teh script to  just scrape your own)
View the content with an online JSON viewer. I'd recommend http://jsoneditoronline.org/. You just use the "Open" button at the top of the page. Also, you can shrink down the (pointless in this case) left pane to view the part we want as full screen.
You should end up with something like this:
 

From here you can click through the hierarchy as you like, identifying datasets, dimensions and dimension items that could be of use to you.
For the developer/data scientist types I've scraped the urls for the various datasets and dimensions as well.
