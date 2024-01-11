# %%
import yfinance as yf
import pandas as pd
from tabulate import tabulate
from fpdf import FPDF

def create_pdf(content, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    pdf.output(filename)

tickers = yf.Tickers('BITI BITO BITX GBTC NDAQ SPYV SPY VBK VBR QQQ VGT')

# Access each ticker using (example)
for ticker in tickers.tickers:
    # Initialize the content string
    content = ""

    # Append title
    content += f"===== {ticker} Info =====\n"
    
    # Print ticker info with indentation
    ticker_info = tickers.tickers[ticker].info.copy()
    ticker_info_str = {str(key): val for key, val in ticker_info.items()}
    content += tabulate(ticker_info_str.items(), tablefmt='plain') + "\n"
    
    # Print a gap
    content += "\n"
    
    # Append title
    content += f"===== {ticker} Historical Data =====\n"
    
    # Convert Timestamps to strings in the historical_data dictionary
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
    content += tabulate(historical_data_table, headers='keys', tablefmt='plain') + "\n"
    
    # Print a gap
    content += "\n"
    
    # Append title
    content += f"===== {ticker} Actions =====\n"
    
    # Convert Series objects to lists in the actions data
    actions = tickers.tickers[ticker].actions.copy()
    actions_str = {str(key): val.tolist() if isinstance(val, pd.Series) else val for key, val in actions.items()}
    content += tabulate(actions_str.items(), tablefmt='plain') + "\n"
    
    # Print a gap
    content += "\n"

    # Create a PDF for each ticker
    pdf_filename = f"{ticker}_output.pdf"
    create_pdf(content, pdf_filename)
    print(f"PDF created: {pdf_filename}")


# %%



