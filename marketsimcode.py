""""""  		  	   		   	 		  		  		    	 		 		   		 		  
"""MC2-P1: Market simulator.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		   	 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		   	 		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		   	 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		   	 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		   	 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		   	 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		   	 		  		  		    	 		 		   		 		  
or edited.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		   	 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		   	 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		   	 		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Student Name: Chi Fai Chan (replace with your name)  		  	   		   	 		  		  		    	 		 		   		 		  
GT User ID: cchan313 (replace with your User ID)  		  	   		   	 		  		  		    	 		 		   		 		  
GT ID: 903645447 (replace with your GT ID)  		  	   		   	 		  		  		    	 		 		   		 		  
"""  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
import datetime as dt  		  	   		   	 		  		  		    	 		 		   		 		  
import os
import numpy as np
import pandas as pd  		  	   		   	 		  		  		    	 		 		   		 		  
from util import get_data, plot_data

def author():
    return "cchan313"
  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
def compute_portvals(  		  	   		   	 		  		  		    	 		 		   		 		  
    orders_data_frame,
    start_val=100000,
    commission=0,
    impact=0,
):  		  	   		   	 		  		  		    	 		 		   		 		  
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    Computes the portfolio values.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
    :param orders_file: Path of the order file or the file object  		  	   		   	 		  		  		    	 		 		   		 		  
    :type orders_file: str or file object  		  	   		   	 		  		  		    	 		 		   		 		  
    :param start_val: The starting value of the portfolio  		  	   		   	 		  		  		    	 		 		   		 		  
    :type start_val: int  		  	   		   	 		  		  		    	 		 		   		 		  
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		   	 		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		   	 		  		  		    	 		 		   		 		  
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		   	 		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		   	 		  		  		    	 		 		   		 		  
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		   	 		  		  		    	 		 		   		 		  
    :rtype: pandas.DataFrame  		  	   		   	 		  		  		    	 		 		   		 		  
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    # this is the function the autograder will call to test your code  		  	   		   	 		  		  		    	 		 		   		 		  
    # NOTE: orders_file may be a string, or it may be a file object. Your  		  	   		   	 		  		  		    	 		 		   		 		  
    # code should work correctly with either input  		  	   		   	 		  		  		    	 		 		   		 		  
    # TODO: Your code here

    # create order dataframe
    orders_df = orders_data_frame.copy()
    dates = orders_df.index.drop_duplicates(keep="first")
    dates = sorted(dates)
    start_date = dates[0]
    end_date = dates[-1]
    dates = pd.date_range(start_date, end_date)
    stocks = set()
    for stock in orders_df.iloc[:,0]:
        stocks.add(stock)

    # create prices dataframe
    prices_df = get_data(stocks, dates)
    prices_df = prices_df.drop("SPY", 1)
    prices_df["Cash"] = 1.0
    dates = prices_df.index.drop_duplicates(keep="first")

    # create trade dataframe
    trade_df = prices_df.copy()
    trade_df[:] = 0
    for date, order in orders_df.iterrows():
        index = str(date.date())
        sym = order[0]
        action = order[1]
        shares = order[-1]
        price = shares * prices_df.loc[index,sym]
        if action == "BUY":
            trade_df.loc[index,sym] = trade_df.loc[index,sym] + shares
            trade_df.loc[index,"Cash"] = trade_df.loc[index,"Cash"] - price - commission - (price *
                                                                                            impact)
        else:
            trade_df.loc[index,sym] = trade_df.loc[index,sym] - shares
            trade_df.loc[index,"Cash"] = trade_df.loc[index,"Cash"] + price - commission - (price *
                                                                                            impact)

    # create holdings dataframe
    stocks.add("Cash")
    holdings_df = trade_df.copy()
    holdings_df["Cash"][0] = holdings_df["Cash"][0] + start_val
    for i in range(1, len(dates)):
        index = dates[i].date()
        pre_index = dates[i-1].date()
        for stock in stocks:
            pre_position = holdings_df.loc[pre_index, stock]
            holdings_df.loc[index, stock] = holdings_df.loc[index, stock] + pre_position

    # create value dataframe
    value_df = prices_df * holdings_df
    portvals = value_df.sum(axis=1)
  		  	   		   	 		  		  		    	 		 		   		 		  
    # In the template, instead of computing the value of the portfolio, we just  		  	   		   	 		  		  		    	 		 		   		 		  
    # read in the value of IBM over 6 months
    return portvals


if __name__ == "__main__":  		  	   		   	 		  		  		    	 		 		   		 		  
    pass
