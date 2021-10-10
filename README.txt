In this project, I have developed technical indicators and a Theoretically Optimal Strategy that will be the ground layer of a later project. The technical indicators developed here will be utilized in a later project to devise an intuition-based trading strategy and a Machine Learning based trading strategy. The Theoretically Optimal Strategy will give a baseline to gauge later project’s performance. 


-markesimcode.py
	-This is a market simulator that accepts trading orders and keeps track of a portfolio's value over time.You can use the market simulator by calling compute_portvals() that returns a 	DataFrame with one column. It adheres to the following API:
		
		compute_portvals(orders_data_frame, start_val, commission, impact)
		
			-orders_data_frame: Dataframe that contains the orders
			-start_val: Starting value of the portfolio
			-commission: The fixed amount in dollars charged for each
			 transaction
			-impact: The amount the price moves against the trader compared to
			 the historical data at each transaction. Impact of 0.01 in the API
			 corresponds to an impact of 1%.
			 
			 
-TheoreticallyOpitmalStrategy.py
	-This is a trading strategy that assumes you can see the future. The strategy is contrained by the portfolio size ($100,000) and order limits (1000 shares long, 1000 shares short, 0 shares). the output result is  You can use the strategy by calling testPolicy(). The output result is a single column data frame, whose values represent trades for each trading day. It adheres to the following API:
	 
		testPolicy(symbol, sd, ed, sv)
		
			-symbol: the stock symbol to act on in string
			-sd: A DateTime object that represents the start date
			-ed: A DateTime object that represents the end date
			-sv: Start value of the portfolio
	 				 

-indicators.py
	-There are 5 technical indicators in the file. They are Price/Simple Moving Average, Bollinger Bands Percentage, Momentum, Commodity Channel Index (CCI), Williams %R. These indicators return one results vector that can be interpreted as actionable buy/sell signals. They adhere to the following API:
	
		price_sma(symbols, start_date, end_date, lookback)
		bbp(symbols, start_date, end_date, lookback)
		momentum(symbols, start_date, end_date, lookback)
		cci(symbols, start_date, end_date, lookback=20)
		will_r(symbols, start_date, end_date, lookback=14)
		
			-symbols: A List or Numpy of the stock symbols to act on
			-start_date: A DateTime object that represents the start date
			-end_date: A DateTime object that represents the end date
			-lookback: An Integer that represents lookback days (William %R at 14 days)
			 

-testproject.py
	-This is a file that uses the market simulator, trading strategy, and technical indicators above to generate charts and statics for reporting purposes. In the part1 function, it produces the necessary charts and statics for the symbol JPM with starting cash/ value at $100,000 during the time period January 1, 2008 to December 31, 2009 by calling the testPolicy function. In the part2 function, it takes the same symbol and date range parameters to call each indicator and produce the necessary charts to best represent each indicator. You can execute the program by calling test_code() or by running the testproject.py file.
