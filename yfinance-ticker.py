#!/usr/bin/env python
# coding: utf-8

# In[31]:


import yfinance as yf
import pandas as pd
from tabulate import tabulate

# Here's the list of stocks that need changed if you wish to see different ones
tickers = yf.Tickers('IBM')

# Access each ticker using (example)
for ticker in tickers.tickers:
    # Print title
    print(f"===== {ticker} Info =====")
    
    # Print ticker info with indentation
    ticker_info = tickers.tickers[ticker].info.copy()
    ticker_info_str = {str(key): val for key, val in ticker_info.items()}
    print(tabulate(ticker_info_str.items(), tablefmt='plain'))
    
    # Print a gap
    print("\n")
    
    # Print title
    print(f"===== {ticker} Historical Data =====")
    
    # Convert Timestamps to strings in the historical_data dictionary since sh*t kept breaking /eyeroll
    historical_data = tickers.tickers[ticker].history(period='1mo')
    historical_data_str = historical_data.reset_index().to_dict(orient='list')
    
    # Convert Series objects to lists
    for key, val in historical_data_str.items():
        if isinstance(val, pd.Series):
            historical_data_str[key] = val.tolist()
        elif isinstance(val[0], pd.Timestamp):
            historical_data_str[key] = [str(date) for date in val]
    
    # Print historical data in a table
    historical_data_table = {k: historical_data_str[k] for k in ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']}
    print(tabulate(historical_data_table, headers='keys', tablefmt='plain'))
    
    # Print a gap
    print("\n")
    
    # Print title
    print(f"===== {ticker} Actions =====")
    
    # Convert Series objects to lists in the actions data
    actions = tickers.tickers[ticker].actions.copy()
    actions_str = {str(key): val.tolist() if isinstance(val, pd.Series) else val for key, val in actions.items()}
    print(tabulate(actions_str.items(), tablefmt='plain'))
    
    # Print a gap
    print("\n")


