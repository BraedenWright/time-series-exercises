import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from math import sqrt
from sklearn.metrics import mean_squared_error



def prep_store_data(df):
    '''
    Takes in store item sales data and sets the index to the datetime, then sorts the data by the new index.
    After, it renames sale_amount and creates columns for Month and Day of the week'''
    # fix time format and set as index
    df.sale_date = df.sale_date.apply(lambda date: date[:-13])
    df.sale_date = pd.to_datetime(df.sale_date, format='%a, %d %b %Y')
    df = df.set_index('sale_date').sort_index()
    
    # rename and add/drop select columns
    df = df.rename(columns={'sale_amount': 'quantity'})
    df = df.drop(columns='item_id')
    df['sales_total'] = df.quantity * df.item_price
    df['month'] = df.index.month_name()
    df['day_of_week'] = df.index.day_name()
    
    return df



def prep_opsd_data(df):
    df.columns = [column.replace('+','_').lower() for column in df]
    df.date = pd.to_datetime(df.date)
    df = df.set_index('date').sort_index()
    df['month'] = df.index.month_name()
    df['year'] = df.index.year
    df = df.fillna(0)
    df['wind_solar'] = df.wind + df.solar
    return df



# provided by Codeup

def evaluate(target_var):
    '''
    This function will take the actual values of the target_var from validate, 
    and the predicted values stored in yhat_df, 
    and compute the rmse, rounding to 0 decimal places. 
    it will return the rmse. 
    '''
    rmse = round(sqrt(mean_squared_error(validate[target_var], yhat_df[target_var])), 0)
    return rmse




# provided by Codeup


def plot_and_eval(target_var):
    '''
    This function takes in the target var name (string), and returns a plot
    of the values of train for that variable, validate, and the predicted values from yhat_df. 
    it will als lable the rmse. 
    '''
    plt.figure(figsize = (12,4))
    plt.plot(train[target_var], label='Train', linewidth=1)
    plt.plot(validate[target_var], label='Validate', linewidth=1)
    plt.plot(yhat_df[target_var])
    plt.title(target_var)
    rmse = evaluate(target_var)
    print(target_var, '-- RMSE: {:.0f}'.format(rmse))
    plt.show()

