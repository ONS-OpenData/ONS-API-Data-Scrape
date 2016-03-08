# -*- coding: utf-8 -*-
"""
Created on Tue Feb 09 11:22:30 2016

@author: Mike

"""

import API_tools as API
import requests
import json
import sys

# =============================================================
# Populate the 1st tier - Using a basic scrape of the dataseat
# =============================================================

def scrape_datasets(context, key):
    
    scrape = {}
    
    dataset_urls = API.dataset_details_url_list(context, key)
    dimension_urls = API.dataset_get_linked_nodes(dataset_urls, 'Dimensions')    
  
    for i in range(0, len(dataset_urls)):          
        # For each dataset
        endpoint = 'http://data.ons.gov.uk/ons/api/data/'
        first_url = endpoint + dataset_urls[i]
        
        try:        
        
            # Make a call to dataset details
            data = requests.get(first_url)
            JSONasDICT = json.loads(data.text)
    
            # Initialise a dictioary for passing all the values in
            tier1 = {}
    
            # To that dictionary add the dataset name
            name = JSONasDICT['ons']['datasetDetail']['names']['name'][0]['$']
            tier1.update({'Name':name})
            
            # The geographic hierarchy
            geo_h = JSONasDICT['ons']['datasetDetail']['geographicalHierarchies']['geographicalHierarchy']['id']
            tier1.update({'Geographical Hierarchy':geo_h})
            
            # is it geographically significant?
            geo_s = JSONasDICT['ons']['datasetDetail']['isGeoSignificant']
            tier1.update({'Is it geographically significant?':geo_s})        
            
            # The Publication date
            pdate = JSONasDICT['ons']['datasetDetail']['publicationDate']
            tier1.update({'Publication Date':pdate})
            
            # The url
            date = JSONasDICT['ons']['datasetDetail']['urls']['url'][1]['href']
            tier1.update({'dataset url':date})
    
            # Store the relevent **dimension** url
            url = endpoint + dimension_urls[i]
            tier1.update({'dimensions url':url})
            
            scrape.update({i:tier1.copy()})            

        except:
            print 'fail - dataset: ', first_url

    return scrape
        


# =============================================================
# Populate the 1st tier - Using a basic scrape of the dataseat
# =============================================================

def scrape_dimension(scrape):   # Note this is one instance of scrape (i.e one 'i' not the whole thing)

    # Try catch so we dont derail for a bad url

    try:        
        
        # Make a call to dataset details
        data = requests.get(scrape['dimensions url'])
        JSONasDICT = json.loads(data.text)
        
        # Find where the object branches
        I_branch_at = JSONasDICT['ons']['dimensionList']['dimension']        
        
        mywrapper = {}
        for i in range(0, len(I_branch_at)):
            
            # Define/Redefine dictioary of what were scraping per dimension item
            mydict = {}
            
            # Scrape the dimension id
            mydict.update({'id':I_branch_at[i]['id']})

            # Scrape the dimension name
            mydict.update({'name':I_branch_at[i]['names']['name'][0]['$']})
            
            # Scrape the dimension url
            url = I_branch_at[i]['urls']['url'][1]['href']
            mydict.update({'dimensions url':url})
            
            # Create a holding space for the dimension items (we'll re-populate with another function later)
            mydict.update({'dimension items':'if you can see me - somethings gone wrong:)'})        
            
            # Wrap the lot for passing to Tier
            mywrapper.update({i:mydict.copy()})  

        # Pass the new data in
        scrape.update({'dimensions':mywrapper.copy()})
        
        return scrape       
    except:
        print 'fail - dimensions:', scrape['dimensions url']   



# =============================================================
# Populate the 3rd tier - getting the dimension items for each dimension
# =============================================================

def scrape_dimension_items(scrape):   # Note this is one instance of scrape (i.e one 'x' within 'i' not the whole thing)

    # Need a global-ish counter so we can track where we are for the failed STATH calls (see except:)
    usecount = 0
    
    # dictionary we're returning
    itemdict = {}
    
    # NOTE we cant API call the geography hierarchies, we'll need the try catch
    url = 'http://data.ons.gov.uk/ons/api/data/' + scrape['dimensions url']

    try:        
        dimdata = requests.get(url)
        JSONasDICT = json.loads(dimdata.text)
        
        I_branch_at = JSONasDICT['Structure']['CodeLists']['CodeList']['Code']
        
        for item in range(0, len(I_branch_at)):

            items = {}
        
            items.update({'name':I_branch_at[item]['Description'][0]['$']})
            
            itemdict.update({item:items.copy()})
            
            usecount += 1
   
    except:
        pass

    try:
        scrape['dimension items'] = itemdict.copy()
        return scrape
    
    except:
        pass            
        

# =============================================================
# Funtion to run the scraper for a single context
# =============================================================

def context_scrape(context, key):
    
    # Initialise
    scrape = scrape_datasets(context, key)
    
    # For each dataset - opulating all dimensions
    for i in scrape:    
        scrape[i] = scrape_dimension(scrape[i])
    
    # For each dimension(within each dataset) poplulate all dimension items
    for i in scrape:
        for x in scrape[i]['dimensions']:
                # pass
                scrape[i]['dimensions'][x] = scrape_dimension_items(scrape[i]['dimensions'][x])
                
    return scrape
    



##########
## MAIN ##
##########

scrape = {}

# Get the key from the command line
key = sys.argv[1]

# Scrape the Economic context
context = 'Economic'
scrape.update({context:context_scrape(context, key)})

# Scrape the social context
context = 'Social'
scrape.update({context:context_scrape(context, key)})

# Scrape the social context
context = 'Census'
scrape.update({context:context_scrape(context, key)})


# create a local JSON dump out of the scrape
with open('WDA_scrape.json', 'w') as fp:
    json.dump(scrape, fp)



