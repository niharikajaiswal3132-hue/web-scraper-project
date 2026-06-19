import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

url = "https://www.bbc.com/news"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

headlines = []

for h in soup.find_all("h2"):
    text = h.get_text().strip()
    
    # CLEANING STEP (remove junk / very short text)
    if text and len(text) > 15:
        headlines.append(text)

# TIMESTAMP (important for real projects)
scraped_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# STRUCTURED DATA
df = pd.DataFrame({
    "Headline": headlines,
    "Scraped_At": [scraped_time] * len(headlines)
})

# SAVE FILE
df.to_csv("output.csv", index=False)

print(f"Done ✔ Scraped {len(headlines)} headlines at {scraped_time}")