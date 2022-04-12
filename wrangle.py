# Basics
import numpy as np
import pandas as pd
import os
import scipy.stats as stats
from pydataset import data
from scipy import math
import requests




def wrangle_items():
    
    filename = 'items.csv'
    
    if os.path.exists(filename):
        print('Reading cleaned data from csv file...')
        return pd.read_csv(filename)
    
    
    # put this first page into a list of dictionaries
    domain = 'https://api.data.codeup.com'
    endpoint = '/api/v1/items'
    items = []

    url = domain + endpoint

    response = requests.get(url)
    data = response.json()
    items.extend(data['payload']['items'])
    
    # Get the next page for items
    url = domain + data['payload']['next_page']

    response = requests.get(url)
    data = response.json()
    items.extend(data['payload']['items'])
    
    # Get the last page for items
    url = domain + data['payload']['next_page']

    response = requests.get(url)
    data = response.json()
    items.extend(data['payload']['items'])
    
    # commit to dataframe and save to .csv
    df = pd.DataFrame(items, index=None)
    df.to_csv(filename, index=False)
    
    print('Downloading data from SQL...')
    print('Saving to .csv')
    return df




def wrangle_stores():
    
    filename = 'stores.csv'
    
    if os.path.exists(filename):
        print('Reading cleaned data from csv file...')
        return pd.read_csv(filename)
    
    domain = 'https://api.data.codeup.com'
    endpoint = '/api/v1/stores'
    stores = []

    url = domain + endpoint

    response = requests.get(url)
    data = response.json()
    stores.extend(data['payload']['stores'])

    df = pd.DataFrame(stores, index=None)
    df.to_csv(filename, index=False)
    
    print('Downloading data from SQL...')
    print('Saving to .csv')
    return df