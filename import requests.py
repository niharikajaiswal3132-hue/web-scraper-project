import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.bbc.com/news"

headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

headlines = []

for h in soup.find_all("h2"):
    text = h.get_text().strip()
    if text:
        headlines.append(text)

print(headlines)   # show output

df = pd.DataFrame(headlines, columns=["Headline"])
df.to_csv("output.csv", index=False)

print("Saved to output.csv ✔")