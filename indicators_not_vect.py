""""""
""" 		  	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		
Student Name: Chi Fai Chan (replace with your name)  		  	   		   	 		  		  		    	 		 		   		 		  
GT User ID: cchan313 (replace with your User ID)  		  	   		   	 		  		  		    	 		 		   		 		  
GT ID: 903645447 (replace with your GT ID)  		  	   		   	 		  		  		    	 		 		   		 		  
"""  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
import datetime as dt  		  	   		   	 		  		  		    	 		 		   		 		  
import os
import numpy as np
import pandas as pd  		  	   		   	 		  		  		    	 		 		   		 		  
from util import get_data, plot_data
import math

def author():
    return "cchan313"

# simple moving average
def smavg(symbols, start_date, end_date, lookback):
    dates = pd.date_range(start_date, end_date)
    price = get_data(symbols, dates)
    sma = price.copy()
    sma = sma.drop("SPY", 1)
    for day in range(price.shape[0]):
        sma.iloc[day,:] = 0
    for day in range(price.shape[0]):
        if day < lookback:
            sma.iloc[day,:] = np.nan
            continue
        for sym in range(len(symbols)):
            for prev_day in range(day-lookback+1, day+1):
                sma.iloc[day,sym] = sma.iloc[day,sym] + price.iloc[prev_day,sym]
        sma.iloc[day,:] = sma.iloc[day,:]/lookback
    return sma

# price/simple moving average
def price_sma(symbols, start_date, end_date, lookback):
    price_sma = smavg(symbols, start_date, end_date, lookback)
    dates = pd.date_range(start_date, end_date)
    price = get_data(symbols, dates)
    for day in range(lookback, price.shape[0]):
        for sym in range(len(symbols)):
            price_sma.iloc[day,sym] = price.iloc[day,sym] / price_sma.iloc[day, sym]
    return price_sma

# Bollinger Band Percentage
def bbp(symbols, start_date, end_date, lookback):
    sma = smavg(symbols, start_date, end_date, lookback)
    dates = pd.date_range(start_date, end_date)
    price = get_data(symbols, dates)
    bbp = price.copy()
    bbp = bbp.drop("SPY", 1)
    for day in range(price.shape[0]):
        bbp.iloc[day, :] = 0
    for day in range(price.shape[0]):
        for sym in range(len(symbols)):
            for prev_day in range(day-lookback+1,day+1):
                bbp.iloc[day,sym] = bbp.iloc[day,sym] + math.pow(price.iloc[prev_day,sym] - sma.iloc[day,sym],2)
            bbp.iloc[day,sym] = math.sqrt(bbp.iloc[day,sym] / (lookback-1))
            bottom = sma.iloc[day,sym] - (2 * bbp.iloc[day,sym])
            top = sma.iloc[day,sym] + (2 * bbp.iloc[day,sym])
            bbp.iloc[day,sym] = (price.iloc[day,sym]-bottom)/(top-bottom)
    return bbp

# Momentum
def momentum(symbols, start_date, end_date, lookback):
    dates = pd.date_range(start_date, end_date)
    price = get_data(symbols, dates)
    momentum = price.copy()
    momentum = momentum.drop("SPY", 1)
    for day in range(price.shape[0]):
        momentum.iloc[day, :] = 0
    for day in range(price.shape[0]):
        if day < lookback:
            momentum.iloc[day, :] = np.nan
            continue
        for sym in range(len(symbols)):
            momentum.iloc[day, sym] = (price.iloc[day, sym] / price.iloc[day-lookback, sym])-1
    return momentum

# Channel Commodity Index (CCI)
def cci(symbols, start_date, end_date, lookback=20):
    sma = smavg(symbols,start_date,end_date,lookback)
    dates = pd.date_range(start_date, end_date)
    price = get_data(symbols, dates)
    cci = price.copy()
    cci = cci.drop("SPY", 1)
    constant = .015
    for day in range(price.shape[0]):
        cci.iloc[day, :] = 0
    for day in range(price.shape[0]):
        if day < lookback:
            cci.iloc[day,:] = np.nan
            continue
        for sym in range(len(symbols)):
            mean_deviation = 0
            for prev_day in range(day - lookback + 1, day + 1):
                mean_deviation = mean_deviation + abs(price.iloc[prev_day,sym] - sma.iloc[day,sym])
            mean_deviation = mean_deviation/lookback
            cci.iloc[day,sym] = (price.iloc[day,sym]-sma.iloc[day,sym]) / (constant*mean_deviation)
    return cci

# William %R
def will_r(symbols, start_date, end_date, lookback=14):
    dates = pd.date_range(start_date, end_date)
    price = get_data(symbols, dates)
    will_r = price.copy()
    will_r = will_r.drop("SPY", 1)
    for day in range(price.shape[0]):
        will_r.iloc[day, :] = 0
    for day in range(price.shape[0]):
        if day < lookback:
            will_r.iloc[day, :] = np.nan
            continue
        for sym in range(len(symbols)):
            lowest_low = price.iloc[day-lookback:day-1,sym].min()
            highest_high = price.iloc[day-lookback:day-1,sym].max()
            will_r.iloc[day,sym] = ((highest_high-price.iloc[day,sym])/(highest_high-lowest_low)) * -100
    will_r[will_r>0] = 0
    will_r[will_r<-100] = -100
    return will_r

  		  	   		   	 		  		  		    	 		 		   		 		  
if __name__ == "__main__":
    sym = ["JPM"]
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    lookback = 5
    sma = smavg(sym,sd,ed,lookback)
    price_sma = price_sma(sym,sd,ed,lookback)
    bbp = bbp(sym,sd,ed,lookback)
    momentum = momentum(sym,sd,ed,lookback)
    cci = cci(sym,sd,ed)
    will_r = will_r(sym,sd,ed)

    file = open("indicators_not_vect.txt", "w")
    file.write(str(will_r))
    file.close()

