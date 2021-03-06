
# LEGACY CODE

The system this was scraping has been closed down by the ONS. This code cannot and will not work any more, I'm keepig this for purposes of my own reference only.


---



NOTE- The datascraper does not currently scrape the Geographic information from the API. I will implement this at some point, but for now just be aware.

# ONS-API-Data-Scrape

A json file (and the script to create it) containing context, name, dimensions and dimension items for all datasets available via the ONS API service.


## About
The idea here is to help non developers to explore the content on the API in detail without having to wade through code documentation (i.e worry about the how you're going to retrieve the data AFTER you've identified something you need).
The scrape is downloadable as a tiered JSON file. Structure wise, it looks like this:

![alt tag](/documentation_images/hierarchy.png)

## How do I use the Scraper?
For exploratory cases (or if you're just curious) it's probably easiest to just download the JSON file on this page. However should you wish to create your own scrape (to get your API key into the urls for example), then navigate to the directory you've downloaded it and the API tools script and use:

```python WDA_Scraper.py "APIkey"```

With "APIkey" being the one you are assigned after signing up to the openAPI BETA - https://www.ons.gov.uk/ons/apiservice/web/apiservice/home


## How do I (a non developer) use the JSON file?
Download WDA_Scrape.json to your PC (or use the script to  just scrape your own)
then view the content with an online JSON viewer. I'd recommend http://jsoneditoronline.org/. You just use the "Open" button at the top of the page. Also, you can shrink down the (pointless in this case) left pane to view the part we want as full screen.

It should then look something like this:

![alt tag](/documentation_images/screenshot.png)

From here you can click through the hierarchy as you like, identifying datasets, dimensions and dimension items that could be of use to you.

For the developer/data scientist we've included urls for the various datasets and dimensions to help get you started.

