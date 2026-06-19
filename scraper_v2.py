import requests
from bs4 import BeautifulSoup
import pandas as pd

data = []

# scrape multiple pages
for page in range(1, 4):
    url = f"http://quotes.toscrape.com/page/{page}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.find_all("div", class_="quote")

    for quote in quotes:
        text = quote.find("span", class_="text").text
        author = quote.find("small", class_="author").text

        data.append({
            "quote": text,
            "author": author,
            "page": page
        })

df = pd.DataFrame(data)

df.drop_duplicates(inplace=True)

df.to_csv("quotes_multi_page.csv", index=False)

print("DONE: Multi-page scraping completed")