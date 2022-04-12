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





def wrangle_sales():
    
    filename = 'sales.csv'
    
    if os.path.exists(filename):
        print('Reading cleaned data from csv file...')
        return pd.read_csv(filename)
    
    
    sales = []
    
    url = 'https://api.data.codeup.com/api/v1/sales?page='
    
    for num in range(1, 184):
        response = requests.get(url + str(num))
        data = response.json()
        sales.extend(data['payload']['sales'])
    
    df = pd.DataFrame(sales)
    df.to_csv(filename, index=False)
    
    print('Downloading data from SQL...')
    print('Saving to .csv')
    return df




def join_to_sales(sales, items, stores):
    
    # rename columns to facilitate merge
    sales = sales.rename(columns={'store': 'store_id', 'item': 'item_id'})
    
    # merge the items and stores to the sales dataframe
    df = pd.merge(sales, items, how='left', on='item_id')
    df = pd.merge(df, stores, how='left', on='store_id')
    
    return df





def wrangle_german_power():
    df = pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')
    return df