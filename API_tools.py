# -*- coding: utf-8 -*-
"""
Created on Tue Feb 09 10:22:09 2016

@author: Mike
"""

import requests
import json

populate_tests = False    # Populates test variales for manual exploration/debugging
                         # Leave it on to poke around in the various called data structure called (i.e browse dictioaries in a variable explorer).
                         # Otherwise turn to false as it slows things down


# ===========================================================================================
# Returns a list of the urls for the DATASET table (one url per economic dataset on the API service).
# ===========================================================================================

def dataset_details_url_list(context, key):   

    payload = {     'apikey': key,     # My, APIKey
                    'context': context,      # Context
                    'from': '01-11-2008',       # Why this date?
    }
    
    endpoint = 'http://data.ons.gov.uk/ons/api/data/datasets.json?'
    
    data = requests.get(endpoint, payload)
    JSONasDICT = json.loads(data.text)
    
    # Find the point where API structure branches to individual datasets
    I_branch_at = JSONasDICT['ons']['datasetList']['contexts']['context']['datasets']['dataset']

    # Get them into a list
    my_list = []
    for i in range(0, len(I_branch_at)):
        my_list.append(I_branch_at[i]['urls']['url'][1]['href'])
    
    return my_list


    
# =================================================================================================
# Returns the urls for the specified nodes (one per url per economic dataset on the API service).
# =================================================================================================

# REQUIRES - the dataset_details_url_list

def dataset_get_linked_nodes(url_list, choice):    # NOTE - dimensions' plural! Table of all dimensions
    
    # Translate the user requested note into the right numer
    whatchoice = {
            'Collection Detail': 0,
            'Datasets':1,
            'Dataset':2,
            'Dsd':3,
            'Set':4,
            'Keyfamily':5,
            'Dimensions':6,
            'Presentation':7,
    }
    endpoint = 'http://data.ons.gov.uk/ons/api/data/'
    
    my_list = [] # Build all out urls
    for url in url_list: 
        url = endpoint + url
        my_list.append(url)
    
    out_list = []    
    for each in my_list: # Itterate them, appending the dataset detauls url to a new list
        data = requests.get(url)
        JSONasDICT = json.loads(data.text)
        node = JSONasDICT['ons']['linkedNodes']['linkedNode'][whatchoice[choice]]['urls']['url'][1]['href']
        out_list.append(node)
        
    return out_list    
      

# =================================================================================================
# =================================================================================================

# ================
# TEST CODE
# ================
if populate_tests == True:
    
    TEST_dataset_details_url_list = dataset_details_url_list()
    TEST_dataset_get_lined_nodes = dataset_get_linked_nodes(TEST_dataset_details_url_list, 'Presentation')
    

    