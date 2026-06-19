import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {"User-Agent": "Mozilla/5.0"}

# ---------- BBC ----------
def scrape_bbc():
    url = "https://www.bbc.com/news"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    data = []

    for h in soup.find_all("h2"):
        text = h.get_text().strip()
        if text and len(text) > 15:
            data.append({"Headline": text, "Source": "BBC"})

    return data


# ---------- TOI ----------
def scrape_toi():
    url = "https://timesofindia.indiatimes.com/home/headlines"
    res = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(res.text, "html.parser")

    data = []

    for tag in soup.find_all(["span", "a"]):
        text = tag.get_text().strip()

        if text and len(text) > 25:
            data.append({"Headline": text, "Source": "TOI"})

    return data


# ---------- FILTER FUNCTION ----------
def filter_news(data, keyword):
    keyword = keyword.lower()
    filtered = []

    for item in data:
        if keyword in item["Headline"].lower():
            filtered.append(item)

    return filtered


# ---------- MAIN ----------
bbc_data = scrape_bbc()
toi_data = scrape_toi()

all_data = bbc_data + toi_data

# USER INPUT FILTER (NEW FEATURE 🔥)
print("\nAvailable filters: AI, sports, business, India, world")
keyword = input("Enter keyword to filter news: ")

if keyword.strip() != "":
    all_data = filter_news(all_data, keyword)

# REMOVE DUPLICATES
seen = set()
unique_data = []

for item in all_data:
    if item["Headline"] not in seen:
        seen.add(item["Headline"])
        unique_data.append(item)

# CATEGORY
for item in unique_data:
    text = item["Headline"].lower()

    if "ai" in text or "tech" in text:
        item["Category"] = "Tech"
    elif "sport" in text or "cricket" in text:
        item["Category"] = "Sports"
    elif "business" in text or "economy" in text:
        item["Category"] = "Business"
    else:
        item["Category"] = "General"

# TIME
time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for item in unique_data:
    item["Scraped_At"] = time_now

# SAVE FILE
df = pd.DataFrame(unique_data)

filename = "output_filtered.csv"
df.to_csv(filename, index=False)

print("\nDone ✔ Smart scraping completed")
print("Total results:", len(unique_data))
print("Saved as:", filename)