""""""
import datetime

"""	  
Student Name: Chi Fai Chan (replace with your name)  		  	   		   	 		  		  		    	 		 		   		 		  
GT User ID: cchan313 (replace with your User ID)  		  	   		   	 		  		  		    	 		 		   		 		  
GT ID: 903645447 (replace with your GT ID)  		  	   		   	 		  		  		    	 		 		   		 		  
"""

import pandas as pd
from util import get_data, plot_data

def author():
    return "cchan313"

def compute_daily_returns(df):
    daily_returns = df.copy()
    daily_returns[1:] = (df[1:] / df[:-1].values) - 1
    if len(daily_returns.shape) == 1:
        daily_returns.iloc[0] = 0
    else:
        daily_returns.iloc[0,:] = 0
    return daily_returns

def testPolicy(symbol, sd, ed, sv):
    bound = 0
    dates = pd.date_range(sd, ed)
    prices_df = get_data([symbol], dates)
    dates = prices_df.index
    df_trades = pd.DataFrame({"Trades": 0}, index=dates)
    prices_df = prices_df.drop("SPY", 1)
    for date in range(0,len(dates)-30):
        price = prices_df.iloc[date].item()
        prices = prices_df.iloc[date:date+30]
        max = prices.max().item()
        min = prices.min().item()
        if((bound == 0) & (price >= max)):
            df_trades.iloc[date] = -1000
            bound = bound - 1000
        elif((bound == 1000) & (price >= max)):
            df_trades.iloc[date] = -2000
            bound = bound - 2000
        elif((bound == 0) & (price <= min)):
            df_trades.iloc[date] = 1000
            bound = bound + 1000
        elif((bound == -1000) & (price <= min)):
            df_trades.iloc[date] = 2000
            bound = bound + 2000
        else:
            pass
    if bound == 1000: df_trades.loc[ed] = -1000
    else: df_trades.loc[ed] = 1000
    return df_trades

if __name__ == "__main__":
    pass

  		  	   		   	 		  		  		    	 		 		   		 		  

