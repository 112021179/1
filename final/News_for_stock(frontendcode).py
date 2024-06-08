import streamlit as st
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import pandas as pd

st.title("Latest Stock News")

# --- Sidebar ---
st.sidebar.header("Latest Stock News")
stock = st.sidebar.text_input("Enter Stock Symbol:",)

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