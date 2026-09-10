import feedparser
import pandas as pd
import os
from datetime import datetime

# ============================
# RSS FEED INDONESIA
# ============================

RSS_FEEDS = [

    {
        "source": "ANTARA",
        "url": "https://www.antaranews.com/rss/terkini.xml"
    },

    {
        "source": "ANTARA Nasional",
        "url": "https://www.antaranews.com/rss/nasional.xml"
    },

    {
        "source": "ANTARA Politik",
        "url": "https://www.antaranews.com/rss/politik.xml"
    }

]

# ============================
# MENAMPUNG DATA
# ============================

news = []

print("=" * 50)
print("Mengambil berita dari RSS...")
print("=" * 50)

for feed in RSS_FEEDS:

    print(f"\nSource : {feed['source']}")

    rss = feedparser.parse(feed["url"])

    print("Jumlah berita :", len(rss.entries))

    for item in rss.entries:

        title = item.get("title", "")

        summary = item.get("summary", "")

        link = item.get("link", "")

        published = item.get("published", "")

        news.append({

            "title": title,

            "content": summary,

            "source": feed["source"],

            "url": link,

            "date": published,

            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "label": 1

        })

# ============================
# DATAFRAME
# ============================

df = pd.DataFrame(news)

# ============================
# HAPUS DUPLIKAT
# ============================

before = len(df)

df.drop_duplicates(

    subset=["title"],

    inplace=True

)

after = len(df)

# ============================
# BUAT FOLDER DATASET
# ============================

os.makedirs("dataset", exist_ok=True)

# ============================
# SIMPAN CSV
# ============================

output = "dataset/rss_news.csv"

df.to_csv(

    output,

    index=False,

    encoding="utf-8-sig"

)

# ============================
# HASIL
# ============================

print("\n" + "=" * 50)

print("RSS BERHASIL")

print("=" * 50)

print("Total berita :", after)

print("Duplikat dihapus :", before - after)

print("Disimpan ke :", output)

print("=" * 50)