from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import pandas as pd

stock = input("Enter the stock symbol: ")
news = {}

url = f'https://finviz.com/quote.ashx?t={stock}&p=d'
request = Request(url=url, headers={'user-agent': 'news_scraper'})
response = urlopen(request)

html = BeautifulSoup(response, features='html.parser')
finviz_news_table = html.find(id='news-table')
news[stock] = finviz_news_table

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

df.to_csv(fr'{stock}.csv', index=False, header=True)