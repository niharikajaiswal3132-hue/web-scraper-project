import requests
from bs4 import BeautifulSoup
import pandas as pd

leads = []

for page in range(1, 4):
    url = f"http://quotes.toscrape.com/page/{page}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.find_all("div", class_="quote")

    for item in items:
        quote = item.find("span", class_="text").text
        author = item.find("small", class_="author").text

        leads.append({
            "business_name": author,
            "description": quote,
            "source_page": page
        })

df = pd.DataFrame(leads)

df.drop_duplicates(inplace=True)

df.to_csv("leads.csv", index=False)

print("DONE: Lead file generated successfully")