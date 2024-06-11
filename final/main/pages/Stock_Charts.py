import yfinance as yf
import streamlit as st
import plotly.express as px  # Use plotly.express for plotting

st.title("📈Stock Data Visualization")

def fetch_stock_data(symbol, period, interval):
    data = yf.download(symbol, period=period, interval=interval)
    return data


def plot_stock_data(data, symbol, company_name, period, interval):
    if data.empty:
        st.error(f"No data available for {symbol} ({company_name}) in selected period and interval.")
        return

    fig = px.line(data, x=data.index, y=["Close", "Open"],
                  labels={"value": "Price", "variable": "Price Data"},
                  title=f"{company_name} ({symbol}) Price Chart ({period}, {interval})")

    # Annotate highest, lowest, and current prices
    highest_price = round(data["Close"].max(), 2)
    lowest_price = round(data["Close"].min(), 2)
    current_price = round(data["Close"].iloc[-1], 2)
    highest_point_time = data["Close"].idxmax()
    lowest_point_time = data["Close"].idxmin()
    current_time = data["Close"].index[-1]

    fig.add_annotation(
        x=highest_point_time,
        y=highest_price,
        text=f"Highest: {highest_price}",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-20,
        font=dict(color="green"),
    )

    fig.add_annotation(
        x=lowest_point_time,
        y=lowest_price,
        text=f"Lowest: {lowest_price}",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=20,
        font=dict(color="red"),
    )

    fig.add_annotation(
        x=current_time,
        y=current_price,
        text=f"Current: {current_price:.2f}",
        showarrow=True,
        arrowhead=1,
        ax=-20,
        ay=-10,
        font=dict(color="blue"),
    )

    fig.update_layout(
        xaxis_title="Date",
        xaxis_tickangle=-45,
    )

    st.plotly_chart(fig)


# Predefined list of valid symbols with company names
valid_symbols = {
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft Corporation',
    'AMZN': 'Amazon.com Inc.',
    'TSLA': 'Tesla Inc.',
    'GOOGL': 'Alphabet Inc. (Google)',
    'META': 'Meta Platforms Inc.',
    'NFLX': 'Netflix Inc.',
    'NVDA': 'NVIDIA Corporation',
    'ADBE': 'Adobe Inc.',
    'CRM': 'Salesforce Inc.',
    'ORCL': 'Oracle Corporation',
    'CSCO': 'Cisco Systems Inc.',
    'INTC': 'Intel Corporation',
    'IBM': 'International Business Machines Corporation',
    'VZ': 'Verizon Communications Inc.',
    'T': 'AT&T Inc.',
    'JPM': 'JPMorgan Chase & Co.',
    'BAC': 'Bank of America Corporation',
    'WFC': 'Wells Fargo & Company',
    'C': 'Citigroup Inc.',
    'GS': 'Goldman Sachs Group Inc.',
    'MS': 'Morgan Stanley',
    'UNH': 'UnitedHealth Group Incorporated',
    'JNJ': 'Johnson & Johnson',
    'PFE': 'Pfizer Inc.',
    'ABT': 'Abbott Laboratories',
    'XOM': 'ExxonMobil Corporation',
    'CVX': 'Chevron Corporation',
    'COP': 'ConocoPhillips',
    'HD': 'The Home Depot Inc.',
    'LOW': 'Lowe\'s Companies Inc.',
    'WMT': 'Walmart Inc.',
    'TGT': 'Target Corporation',
    'COST': 'Costco Wholesale Corporation',
    'NKE': 'Nike Inc.',
    'MCD': 'McDonald\'s Corporation',
    'SBUX': 'Starbucks Corporation',
    'DIS': 'The Walt Disney Company',
    'CMCSA': 'Comcast Corporation',
    'F': 'Ford Motor Company',
    'GM': 'General Motors Company',
    'BA': 'The Boeing Company',
    'UAL': 'United Airlines Holdings Inc.',
    'DAL': 'Delta Air Lines Inc.',
    'LUV': 'Southwest Airlines Co.',
    'AAL': 'American Airlines Group Inc.'
}

# Display symbol and company name in the selectbox
symbol_options = [f"{symbol} ({company_name})" for symbol, company_name in valid_symbols.items()]

symbol = st.selectbox("Select a stock symbol:", symbol_options)

# Extract the symbol from the selected option
symbol = symbol.split(" (")[0]

period = st.selectbox("Select the period for the stock data",
                      ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'], index=5)
interval = st.selectbox("Select the interval for the stock data",
                        ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'], index=9)

if symbol:
    company_name = valid_symbols[symbol]  # Get company name from dictionary
    data = fetch_stock_data(symbol, period, interval)
    plot_stock_data(data, symbol, company_name, period, interval)
    
    st.download_button(
        label = "Download as CSV",
        data = data.to_csv(index = False),
        file_name = f"{symbol}.csv",
        mime = "text/csv",
    )