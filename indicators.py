""""""
""" 		  	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		
Student Name: Chi Fai Chan (replace with your name)  		  	   		   	 		  		  		    	 		 		   		 		  
GT User ID: cchan313 (replace with your User ID)  		  	   		   	 		  		  		    	 		 		   		 		  
GT ID: 903645447 (replace with your GT ID)  		  	   		   	 		  		  		    	 		 		   		 		  
"""
import numpy as np
import pandas as pd
from util import get_data, plot_data


def author():
    return "cchan313"

# Simple Moving Average
def smavg(symbols, start_date, end_date, lookback):
    dates = pd.date_range(start_date, end_date)
    price = get_data(symbols, dates)
    price = price.drop("SPY",1)
    price = price/price.iloc[0]
    sma = price.cumsum()
    sma.values[lookback:,:] = (sma.values[lookback:,:] - sma.values[:-lookback,:]) / lookback
    sma.iloc[:lookback,:] = np.nan
    return sma

# Price/Simple Moving Average
def price_sma(symbols, start_date, end_date, lookback):
    price_sma = smavg(symbols, start_date, end_date, lookback)
    dates = pd.date_range(start_date, end_date)
    price = get_data(symbols, dates)
    price = price.drop("SPY",1)
    price = price / price.iloc[0]
    price_sma = price/price_sma
    return price_sma

# Bollinger Band Percentage
def bbp(symbols, start_date, end_date, lookback):
    sma = smavg(symbols, start_date, end_date, lookback)
    dates = pd.date_range(start_date, end_date)
    price = get_data(symbols, dates)
    price = price.drop("SPY",1)
    price = price/price.iloc[0]
    rolling_std = price.rolling(window=lookback, min_periods=lookback).std()
    top_band = sma + (2 * rolling_std)
    bottom_band = sma - (2 * rolling_std)
    bbp = (price - bottom_band) / (top_band - bottom_band)
    return bbp

# Momentum
def momentum(symbols, start_date, end_date, lookback):
    dates = pd.date_range(start_date, end_date)
    price = get_data(symbols, dates)
    price = price.drop("SPY",1)
    price = price/price.iloc[0]
    momentum = price.copy()
    for day in range(price.shape[0]):
        momentum.iloc[day,:] = 0
    for day in range(price.shape[0]):
        if day < lookback-1:
            momentum.iloc[day,:] = np.nan
            continue
        momentum.iloc[day,:] = (price.iloc[day,:] / price.iloc[day-lookback+1,:]) - 1
    return momentum

# Channel Commodity Index (CCI)
def cci(symbols, start_date, end_date, lookback=20):
    sma = smavg(symbols, start_date, end_date, lookback)
    dates = pd.date_range(start_date, end_date)
    price = get_data(symbols, dates)
    price = price.drop("SPY",1)
    price = price/price.iloc[0]
    cci = price.copy()
    constant = .015
    for day in range(price.shape[0]):
        cci.iloc[day,:] = 0
    for day in range(price.shape[0]):
        if day < lookback-1:
            cci.iloc[day, :] = np.nan
            continue
        mean_deviation = 0
        mean_deviation = (abs(price.iloc[day-lookback+1:day+1,:]-sma.iloc[day,:])).sum()
        mean_deviation = mean_deviation/lookback
        cci.iloc[day,:] = (price.iloc[day,:] - sma.iloc[day,:]) / (constant * mean_deviation)
    return cci

# William %R
def will_r(symbols, start_date, end_date, lookback=14):
    dates = pd.date_range(start_date, end_date)
    price = get_data(symbols, dates)
    price = price.drop("SPY",1)
    price = price/price.iloc[0]
    will_r = price.copy()
    for day in range(price.shape[0]):
        will_r.iloc[day, :] = 0
    for day in range(price.shape[0]):
        if day < lookback-1:
            will_r.iloc[day, :] = np.nan
            continue
        lowest_low = price.iloc[day-lookback+1:day+1,:].min()
        highest_high = price.iloc[day-lookback+1:day+1,:].max()
        will_r.iloc[day,:] = ((highest_high - price.iloc[day,:]) / (highest_high - lowest_low)) * -100
    return will_r


if __name__ == "__main__":
    pass
