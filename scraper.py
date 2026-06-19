import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "http://quotes.toscrape.com"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

data = []
quotes = soup.find_all("div", class_="quote")

for quote in quotes:
    text = quote.find("span", class_="text").text
    author = quote.find("small", class_="author").text

    data.append({
        "quote": text,
        "author": author
    })

df = pd.DataFrame(data)

df.to_csv("quotes.csv", index=False)

print("DONE: Scraping completed successfully")