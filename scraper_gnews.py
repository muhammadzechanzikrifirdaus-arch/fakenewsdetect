import requests
import pandas as pd
import os
from datetime import datetime

# ===================================
# API KEY GNEWS
# ===================================

API_KEY = "6afc5216b17282ba52c794d2cfb81ddf"

URL = (
    "https://gnews.io/api/v4/search?"
    "q=Indonesia"
    "&lang=id"
    "&country=id"
    "&max=100"
    "&sortby=publishedAt"
    f"&apikey={API_KEY}"
)

# ===================================
# REQUEST API
# ===================================

print("=" * 50)
print("Mengambil berita dari GNews...")
print("=" * 50)

response = requests.get(URL)

if response.status_code != 200:

    print("ERROR :", response.status_code)
    print(response.text)
    exit()

json_data = response.json()

articles = json_data.get("articles", [])

print("Jumlah berita :", len(articles))

# ===================================
# SIMPAN DATA
# ===================================

news = []

for article in articles:

    title = article.get("title", "")

    description = article.get("description", "")

    content = article.get("content", "")

    full_content = description + " " + content

    source = article["source"]["name"]

    url = article.get("url", "")

    image = article.get("image", "")

    published = article.get("publishedAt", "")

    news.append({

        "title": title,

        "content": full_content,

        "source": source,

        "url": url,

        "image": image,

        "date": published,

        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "label": 1

    })

# ===================================
# DATAFRAME
# ===================================

df = pd.DataFrame(news)

# ===================================
# HAPUS DUPLIKAT
# ===================================

before = len(df)

df.drop_duplicates(

    subset=["title"],

    inplace=True

)

after = len(df)

# ===================================
# BUAT FOLDER
# ===================================

os.makedirs(

    "dataset",

    exist_ok=True

)

# ===================================
# SIMPAN CSV
# ===================================

output = "dataset/gnews_news.csv"

df.to_csv(

    output,

    index=False,

    encoding="utf-8-sig"

)

# ===================================
# HASIL
# ===================================

print()

print("=" * 50)

print("SCRAPING GNEWS BERHASIL")

print("=" * 50)

print("Total berita :", after)

print("Duplikat :", before - after)

print("File :", output)

print("=" * 50)