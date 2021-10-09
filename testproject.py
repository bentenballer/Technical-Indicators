""""""
"""		   	 		  		  		    	 		 		   		 		  		  	   		   	 		  		  		    	 		 		   		 		  
Student Name: Chi Fai Chan (replace with your name)  		  	   		   	 		  		  		    	 		 		   		 		  
GT User ID: cchan313 (replace with your User ID)  		  	   		   	 		  		  		    	 		 		   		 		  
GT ID: 903645447 (replace with your GT ID)  		  	   		   	 		  		  		    	 		 		   		 		  
"""
from TheoreticallyOptimalStrategy import compute_daily_returns, testPolicy
from marketsimcode import compute_portvals
from util import get_data
import indicators as id
import datetime as dt
import numpy as np
import pandas as pd
import timeit
import matplotlib.pyplot as plt


def author():
    return "cchan313"

# Part 1:  Theoretically Optimal Strategy
def part1(sd,ed):
    sym = "JPM"
    sv = 100000
    orders = {"Symbol": ["JPM", "JPM"], "Order": ["BUY", "BUY"], "Shares": [1000, 0]}
    benchmark_order = pd.DataFrame(orders, index=[dt.datetime(2008, 1, 2), ed])
    benchmark = compute_portvals(benchmark_order, start_val=sv, commission=0, impact=0)
    benchmark = benchmark / benchmark[0]

    optimal = testPolicy(sym, sd, ed, sv)
    optimal = optimal[optimal != 0].dropna()
    optimal["Symbol"] = "JPM"
    optimal.loc[optimal["Trades"] < 0, "Order"] = "SELL"
    optimal.loc[optimal["Trades"] > 0, "Order"] = "BUY"
    optimal["Shares"] = abs(optimal["Trades"])
    optimal = optimal.drop("Trades", axis=1)
    optimal_port = compute_portvals(optimal, start_val=sv, commission=0, impact=0)
    optimal_port = optimal_port / optimal_port[0]

    ax = benchmark.plot(color="green", label="Benchmark", legend=True)
    optimal_port.plot(ax=ax, color="red", label="Optimal Portfolio", legend=True)
    plt.title("Part 1: Benchmark vs Theoretically Optimal Portfolio")
    plt.ylabel("Normalized Portfolio Value")
    plt.xlabel("Dates")
    plt.savefig("p6_part1.png")

    benchmark_daily_return = compute_daily_returns(benchmark)
    benchmark_daily_return = benchmark_daily_return[1:]
    optimal_daily_return = compute_daily_returns(optimal_port)
    optimal_daily_return = optimal_daily_return[1:]

    benchmark_adr = benchmark_daily_return.mean()
    optimal_adr = optimal_daily_return.mean()
    benchmark_std = benchmark_daily_return.std()
    optimal_std = optimal_daily_return.std()
    benchmark_cr = (benchmark[-1] / benchmark[0]) - 1
    optimal_cr = (optimal_port[-1] / optimal_port[0]) - 1

    file = open("p6_results.txt", "w")
    stats = {"Cumulative Return": [benchmark_cr, optimal_cr], "Stdev of Daily Return": [benchmark_std, optimal_std],
             "Mean of Daily Return": [benchmark_adr, optimal_adr]}
    table = pd.DataFrame(stats, index=["Benchmark", "Optimal"])
    file.write(str(table))
    file.write(f"\n\nBenchmark Ending Value: {benchmark[-1]}")
    file.write(f"\nOptimal Portfolio Ending Value: {optimal_port[-1]}")
    file.close()
    return

# Part 2: Technical Indicators
"""
APIs:
    simple moving average: smavg(symbols,start_date,end_date,lookback)
    price/ simple moving average: price_sma(symbols,start_date,end_date,lookback)
    bollinger band percentage: bbp(symbols,start_date,end_date,lookback)
    momentum: momentum(symbols,start_date,end_date,lookback)
    channel commodity index: cci(symbols,start_date,end_date,lookback=20)
    will_r: will_r(symbols,start_date,end_date,lookback=14)
"""
def part2(sd,ed):
    lookback = 20
    syms = np.array(["JPM"])
    dates = pd.date_range(sd, ed)
    price = get_data(syms, dates)
    price = price.drop("SPY", 1)
    normed = price / price.iloc[0]
    sma = id.smavg(syms,sd,ed,lookback=lookback)
    price_sma = id.price_sma(syms,sd,ed,lookback=lookback)
    bbp = id.bbp(syms,sd,ed,lookback=lookback)
    momentum = id.momentum(syms,sd,ed,lookback=lookback)
    cci = id.cci(syms,sd,ed)
    will_r = id.will_r(syms,sd,ed)

    # indicator#1: Price/SMA
    fig, ax = plt.subplots(figsize=(10,5))
    plt.title("Indicator 1: Price/Simple Moving Average")
    ax1 = ax.twinx()
    ax.plot(normed,color="green")
    sma.plot(ax=ax, color="red")
    price_sma.plot(ax=ax1, color="blue")
    ax.legend(["JPM", "SMA"],loc="upper left")
    ax.set_ylabel("Normalized Stock Price",color="g")
    ax.set_xlabel("Date")
    ax1.legend(["Price/SMA Ratio"],loc="upper right")
    ax1.set_ylabel("Ratio",color="b")
    plt.savefig("p6_part2_sma.png")

    # indicator#2: Bollinger Band Percentage
    rolling_std = normed.rolling(window=lookback, min_periods=lookback).std()
    upper = sma + (2 * rolling_std)
    bottom = sma - (2 * rolling_std)
    figure, ax2 = plt.subplots(nrows=2,ncols=1,sharex=True,sharey=False)
    ax2[0].title.set_text("Indicator 2: Bollinger Band Percentage")
    normed.plot(ax=ax2[0],color="green")
    upper.plot(ax=ax2[0], color="blue")
    bottom.plot(ax=ax2[0], color="blue")
    bbp.plot(ax=ax2[1],color="red")
    ax2[0].legend(["JPM", "Bollinger Band"])
    ax2[0].set_ylabel("Normalized Stock Price")
    ax2[1].set_ylabel("Percentage")
    ax2[1].set_xlabel("Dates")
    ax2[1].legend(["Bollinger Band %"])
    plt.savefig("p6_part2_bbp.png")

    # indicator#3: Momentum
    fig, ax3 = plt.subplots(figsize=(10, 5))
    plt.title("Indicator 3: Momentum")
    ax4 = ax3.twinx()
    ax3.plot(normed, color="green")
    momentum.plot(ax=ax4, color="red")
    ax3.legend(["JPM"],loc="upper left")
    ax4.legend(["Momentum"], loc="upper right")
    ax3.set_ylabel("Normalized Stock Price", color="g")
    ax3.set_xlabel("Date")
    ax4.set_ylabel("Momentum", color="r")
    plt.savefig("p6_part2_momentum.png")

    # indicator#4: Channel Commodity Index (CCI)
    figure, ax5 = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=False)
    ax5[0].title.set_text("Indicator 4: Channel Commodity Index (CCI)")
    normed.plot(ax=ax5[0],color="green")
    cci.plot(ax=ax5[1],color="red")
    ax5[0].legend(["JPM"])
    ax5[0].set_ylabel("Normalized Stock Price")
    ax5[1].set_ylabel("Score")
    ax5[1].set_xlabel("Dates")
    ax5[1].legend(["CCI Score"])
    plt.savefig("p6_part2_cci.png")

    # indicator#5: William %R
    figure, ax6 = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=False)
    ax6[0].title.set_text("Indicator 5: William %R")
    normed.plot(ax=ax6[0], color="green")
    will_r.plot(ax=ax6[1], color="red")
    ax6[0].legend(["JPM"])
    ax6[0].set_ylabel("Normalized Stock Price")
    ax6[1].set_ylabel("Score")
    ax6[1].set_xlabel("Dates")
    ax6[1].legend(["William %R Score"])
    plt.savefig("p6_part2_will_r.png")

    return

def test_code():
    sd = dt.datetime(2008,1,1)
    ed = dt.datetime(2009,12,31)
    part1(sd,ed)
    part2(sd,ed)
    return
  		  	   		   	 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		   	 		  		  		    	 		 		   		 		  
    test_code()  		  	   		   	 		  		  		    	 		 		   		 		  
