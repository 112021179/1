import streamlit as st
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import pandas as pd

st.title("Latest Stock News")

# --- Sidebar ---
st.sidebar.header("Latest Stock News")

# List of popular US stocks (you can add more to this list)
stock_options = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Tesla": "TSLA",
    "Google": "GOOGL",
    "Facebook (Meta)": "META",
    "Netflix": "NFLX",
    "NVIDIA": "NVDA",
    "Adobe": "ADBE",
    "Salesforce": "CRM",
    "Oracle": "ORCL",
    "Cisco": "CSCO",
    "Intel": "INTC",
    "IBM": "IBM",
    "Verizon": "VZ",
    "AT&T": "T",
    "JPMorgan Chase": "JPM",
    "Bank of America": "BAC",
    "Wells Fargo": "WFC",
    "Citigroup": "C",
    "Goldman Sachs": "GS",
    "Morgan Stanley": "MS",
    "UnitedHealth Group": "UNH",
    "Johnson & Johnson": "JNJ",
    "Pfizer": "PFE",
    "Abbott Laboratories": "ABT",
    "ExxonMobil": "XOM",
    "Chevron": "CVX",
    "ConocoPhillips": "COP",
    "Home Depot": "HD",
    "Lowe's": "LOW",
    "Walmart": "WMT",
    "Target": "TGT",
    "Costco": "COST",
    "Nike": "NKE",
    "McDonald's": "MCD",
    "Starbucks": "SBUX",
    "Disney": "DIS",
    "Comcast": "CMCSA",
    "Ford": "F",
    "General Motors": "GM",
    "Boeing": "BA",
    "United Airlines": "UAL",
    "Delta Air Lines": "DAL",
    "Southwest Airlines": "LUV",
    "American Airlines": "AAL",
}

# Dropdown for stock selection
stock_symbol = st.sidebar.selectbox("Choose a Stock:", list(stock_options.keys()))
stock = stock_options[stock_symbol] if stock_symbol else None  # Get the symbol

# --- Main Content ---
if stock:
    news = {}

    url = f'https://finviz.com/quote.ashx?t={stock}&p=d'
    request = Request(url=url, headers={'user-agent': 'news_scraper'})
    response = urlopen(request)

    html = BeautifulSoup(response, features='html.parser')
    finviz_news_table = html.find(id='news-table')
    if finviz_news_table:
        news[stock] = finviz_news_table
    else:
        st.error(f"News table not found for {stock}")

    news_parsed = []
    if stock in news:
        for row in news[stock].findAll('tr'):
            try:
                headline = row.a.getText()
                link = row.a['href']
                source = row.span.getText()
                news_parsed.append([stock, headline, link, source])
            except:
                pass

    df = pd.DataFrame(news_parsed, columns=['Stock', 'Headline', 'Link', 'Source'])

    # Display the DataFrame as a table with clickable links
    st.subheader(f"News for {stock}")
    for index, row in df.iterrows():
        st.markdown(f"[{row['Headline']}]({row['Link']}) - {row['Source']}")

    # Download CSV
    st.download_button(
        label="Download as CSV",
        data=df.to_csv(index=False),
        file_name=f"{stock}_news.csv",
        mime="text/csv",
    )
