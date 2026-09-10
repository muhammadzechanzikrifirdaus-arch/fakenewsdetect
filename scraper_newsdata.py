import requests
import pandas as pd
import os
from datetime import datetime

# ============================================
# API KEY
# ============================================

API_KEY = "pub_243fed91854b4f28a3963f0b05b7e3e3"

url = (
    "https://newsdata.io/api/1/latest"
    f"?apikey={API_KEY}"
    "&country=id"
    "&language=id"
)

print("=" * 50)
print("Mengambil berita dari NewsData...")
print("=" * 50)

response = requests.get(url)

if response.status_code != 200:
    print(response.text)
    exit()

json_data = response.json()

articles = json_data.get("results", [])

print("Jumlah berita :", len(articles))

news = []

for article in articles:

    news.append({

        "title": article.get("title",""),

        "content": article.get("description",""),

        "source": article.get("source_name",""),

        "url": article.get("link",""),

        "date": article.get("pubDate",""),

        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "label":1

    })

df = pd.DataFrame(news)

df.drop_duplicates(
    subset=["title"],
    inplace=True
)

os.makedirs("dataset",exist_ok=True)

df.to_csv(

    "dataset/newsdata_news.csv",

    index=False,

    encoding="utf-8-sig"

)

print()
print("="*50)
print("NEWSDATA BERHASIL")
print("="*50)
print("Total :",len(df))
print("="*50)