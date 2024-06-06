import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import os 
from fsearch import load_valid_symbols, find_similar_symbols

def check_stock_symbol(symbol, valid_symbols):
    if symbol in valid_symbols:
        return True
    
    else:
        similar_symbols = find_similar_symbols(symbol, valid_symbols)
        print(f"Did you mean one of the following? {similar_symbols} \nIf not please try again.")
        return False
    
def fetch_stock_data(symbol):
        default_period = '1y'
        default_interval = '5d' 
        
        user_period = input(f"Enter the period for the stock data (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max) or press ENTER for default value {default_period}: ")
        if not user_period:
            user_period = default_period
        
        user_interval = input(f"Enter the interval for the stock data (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo): or press ENTER for default value {default_interval}:")
        if not user_interval:
            user_interval = default_interval
        
        # for now no checks on user input, i dont care 
        # Want to see this ^^ implemented in the gui version as buttons or dropdowns
        data = yf.download(symbol, period=user_period, interval=user_interval)
        data.to_csv(f'{symbol}_stock_data.csv')
        print(f"Stock data saved to: {os.path.abspath(f'{symbol}_stock_data.csv')}")
 

def get_stock_price(symbol):
    stock = yf.Ticker(symbol)
    price = stock.info['regularMarketPrice']
    return price

def plot_stock_from_csv(symbol):
    
    data = pd.read_csv(f'{symbol}_stock_data.csv')
    if data.empty:
        print(f"No data available for {symbol} in selected period and interval.")
    
    date_column = 'Datetime' if 'Datetime' in data.columns else 'Date'
    data[date_column] = pd.to_datetime(data[date_column])  # Ensure the column is in datetime format
    data.set_index(date_column, inplace=True)
    
    close_prices = data['Close']
    open_prices = data['Open']
    highest_price = round(close_prices.max(), 2)
    lowest_price = round(close_prices.min(), 2)
    current_price = round(close_prices.iloc[-1], 2)
    highest_point_time = close_prices.idxmax()
    lowest_point_time = close_prices.idxmin()
    current_time = close_prices.index[-1]
   
    plt.figure(figsize=(12, 7))
    close_prices.plot(label='Close Prices', color = 'red')
    open_prices.plot(label='Open Prices', linestyle='--', color='green')
    
    plt.annotate(f'Highest: {highest_price}',
                xy=(highest_point_time, highest_price),
                xytext=(highest_point_time, highest_price + (highest_price*0.005)),
                arrowprops=dict(facecolor='green', arrowstyle='->, head_width=0.5, head_length=0.5'),
                horizontalalignment='center', verticalalignment='top')

   
    plt.annotate(f'Lowest: {lowest_price}', 
                xy=(lowest_point_time, lowest_price), 
                xytext=(lowest_point_time, lowest_price - (lowest_price * 0.005)),  # Adjust text position
                arrowprops=dict(facecolor='red', arrowstyle='->, head_width=0.5, head_length=0.5'),
                horizontalalignment='center', verticalalignment='top')

  
    plt.annotate(f'Current: {current_price:.2f}', 
                xy=(current_time, current_price), 
                xytext=(current_time - pd.Timedelta(minutes=5), current_price + (current_price * 0.002)),
                textcoords='data', 
                arrowprops=dict(arrowstyle="fancy", color='blue', 
                                connectionstyle="arc3,rad=.5"))

     
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()

# for the most part all this code ^^ does is just plottinng the stock data


def symbol_input():
    symbol = input("Enter a stock symbol: ").upper()
    
    if check_stock_symbol(symbol, valid_symbols):
        return symbol
    return symbol_input()



valid_symbols = load_valid_symbols('screener.csv')
symbol = symbol_input()
check_stock_symbol(symbol, valid_symbols)

if os.path.exists(f'{symbol}_stock_data.csv'):
    
    if input(f"Stock data for {symbol} already exists. Do you want to fetch new data? (y/n): ").lower() == 'y':
        os.remove(f'{symbol}_stock_data.csv')
        fetch_stock_data(symbol)
        
else:
    fetch_stock_data(symbol)
    
plot_stock_from_csv(symbol)