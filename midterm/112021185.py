import requests
from bs4 import BeautifulSoup
import pandas as pd

current_page = 1

Data=[]

Proceed = True

while(Proceed):
    print("scraping page number: "+str(current_page))

    url = "https://books.toscrape.com/catalogue/page-"+str(current_page)+".html"

    page= requests.get(url)

    soup = BeautifulSoup(page.text,"html.parser")

    if soup.title.text =="404 Not Found":
        Proceed= False
    else:
        all_books=soup.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

    for books in all_books:
        item={}

        item['title']=books.find("img").attrs['alt']

        item['link']=books.find("a").attrs['href']

        item['price']=books.find("p",class_="price_color").text[1:]

        item['avail']=books.find("p",class_="instock availability").text.strip()

        Data.append(item)

    current_page +=1

df=pd.DataFrame(Data)
df.to_csv("books.csv")
