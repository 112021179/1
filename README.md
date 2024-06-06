# Stock Data Visualization Tool

This project is a Python-based tool that allows users to fetch historical stock data for specific stocks, verify the validity of stock symbols, suggest similar symbols for incorrect entries, and visualize stock data through plots. It uses `yfinance` for fetching stock data, `pandas` for data manipulation, and `matplotlib` for plotting the stock prices over time.

## Features

- **Symbol Verification**: Checks if the entered stock symbol is valid and suggests similar symbols if the entered one is incorrect.
- **Fetch Stock Data**: Allows fetching historical stock data based on custom time periods and intervals.
- **Data Visualization**: Visualizes the stock's open and close prices over the selected period, highlighting the highest, lowest, and current prices.
- **Ease of Use**: Simple CLI interface for fetching and visualizing stock data.

## Installation

To run this project, you will need Python 3.6 or later. Clone the repository and install the required dependencies.

```bash
git clone <repository-url>
cd <repository-folder>
pip install -r requirements.txt
```
## Dependencies
- **yfinance**: Used for fetching stock data.
- **matplotlib**: For plotting stock data.
- **pandas**: For data manipulation and analysis.
- **fuzzywuzzy**: For fuzzy stock symbol search.

You can install these dependencies directly using:

```bash
pip install -r requirements.txt
```

## Usage

Run the main script from the command line:

```bash
python main.py
```

The program will prompt you to enter a stock symbol. 
If the symbol is valid, it will then ask for the period and interval for the stock data you want to fetch. 
After fetching the data, it will automatically plot the stock's open and close prices over the selected period.
