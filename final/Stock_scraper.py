from bs4 import BeautifulSoup
import requests
import csv

def scrape_stock_info(stock_symbol):
    url = f"https://finance.yahoo.com/quote/{stock_symbol}"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        price_element = soup.find('fin-streamer', class_='livePrice svelte-mgkamr')
        price = price_element.text.strip() if price_element else None

        name_element = soup.find('h1', class_ ="svelte-3a2v0c")
        name = name_element.text.strip() if name_element else None

        return {'Stock Name': name, 'Stock Price': price}
    else:
        print(f"Error: Failed to retrieve webpage for stock symbol {stock_symbol}")
        return None
    

def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data.keys())
        writer.writeheader()
        writer.writerow(data)

symbol = str(input("Enter the stock symbol(): "))
symbols = (symbol.upper()).split(" ")
for s in symbols:
    stock_data = scrape_stock_info(s)
    if stock_data:
        save_to_csv(stock_data, f"{s}_data.csv")
        print(f"Stock information for {s} has been saved to {s}_data.csv")
    else:
        print(f"There is no stock information for {s}")