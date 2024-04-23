import requests
from bs4 import BeautifulSoup

r = input("Enter which city would you like to search for: ").lower()
query = f'{r}'
url = f'https://www.google.com/search?q=weather+{query}'

response = requests.get(url, headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'})
soup = BeautifulSoup(response.content, 'html.parser')

temperature = soup.find('span', {'id': 'wob_tm'})
if temperature:
    print(f'The current temperature in {query} is: {temperature.text}°C')
else:
    print('Could not find the current temperature.')

precipitation = soup.find('span',{'id': 'wob_pp'})
if precipitation:
    print(f'The current precipitation in {query} is: {precipitation.text}')
else:
    print('Could not find the current precipitation.')

humidity = soup.find('span', {'id' : 'wob_hm'})
if humidity:
    print(f'The current humidity in {query} is: {humidity.text}')
else:
    print('Could not find the current humidity')

wind = soup.find('span', {'id' : 'wob_ws'})
if wind:
    print(f'The current wind in {query} is: {wind.text}')
else:
    print('Could not find the current wind information')

    