import pandas as pd
import os

# ==========================================================
# FUNGSI MEMBACA CSV
# ==========================================================

def load_csv(path):

    if os.path.exists(path):
        print(f"✔ Membaca {path}")
        return pd.read_csv(path)

    print(f"⚠ {path} tidak ditemukan")
    return pd.DataFrame()


# ==========================================================
# DATASET BERITA VALID (KAGGLE)
# ==========================================================

real = load_csv("dataset/data.csv")

if not real.empty:

    # Mencari nama kolom secara otomatis
    title_col = None
    content_col = None

    for col in real.columns:

        c = col.lower()

        if c in ["title", "judul"]:
            title_col = col

        if c in ["content", "text", "isi", "article"]:
            content_col = col

    if title_col is None:
        title_col = real.columns[0]

    if content_col is None:
        content_col = real.columns[1]

    real = real[[title_col, content_col]]

    real.columns = ["title", "content"]

    real["label"] = 1


# ==========================================================
# RSS
# ==========================================================

rss = load_csv("dataset/rss_news.csv")

if not rss.empty:

    rss = rss[["title", "content", "label"]]


# ==========================================================
# GNEWS
# ==========================================================

gnews = load_csv("dataset/gnews_news.csv")

if not gnews.empty:

    gnews = gnews[["title", "content", "label"]]


# ==========================================================
# NEWSDATA
# ==========================================================

newsdata = load_csv("dataset/newsdata_news.csv")

if not newsdata.empty:

    newsdata = newsdata[["title", "content", "label"]]

# ==========================================================
# DATASET HOAX
# ==========================================================

hoax = load_csv(
    "dataset/Indonesia Political Hoax Dataset/combined_train.csv"
)

if not hoax.empty:
    content_column = None

    for col in hoax.columns:
        c = col.lower()
        if c in ["cleaned", "content", "text", "isi"]:
            content_column = col
            break

    if content_column is None:
        content_column = hoax.columns[0]

    hoax = hoax[[content_column, "label"]].copy()
    hoax.columns = ["content", "label"]

    # =====================================================
    # Dataset asli:
    # 1 = HOAX
    # 0 = FAKTA
    # =====================================================

    hoax["label"] = hoax["label"].replace({
        1: 0,
        0: 1
    })

    hoax["title"] = ""

frames = []
for df in [
    real,
    rss,
    gnews,
    newsdata,
    hoax
]:

    if not df.empty:
        frames.append(df)
dataset = pd.concat(

    frames,

    ignore_index=True

)

# ==========================================================
# MEMBERSIHKAN
# ==========================================================

dataset.fillna("", inplace=True)

dataset["title"] = dataset["title"].astype(str)

dataset["content"] = dataset["content"].astype(str)

dataset["text"] = (

    dataset["title"]

    + " "

    + dataset["content"]

)

dataset["text"] = dataset["text"].str.replace(
    "\n",
    " ",
    regex=False
)

dataset["text"] = dataset["text"].str.replace(
    "\r",
    " ",
    regex=False
)

dataset["text"] = dataset["text"].str.strip()

# hapus berita kosong

dataset = dataset[dataset["text"].str.len() > 30]

# hapus duplikat

dataset.drop_duplicates(

    subset=["text"],

    inplace=True

)

dataset.reset_index(

    drop=True,

    inplace=True

)

# hanya simpan text dan label

dataset = dataset[["text", "label"]]

# ==========================================================
# SIMPAN
# ==========================================================

os.makedirs(

    "dataset",

    exist_ok=True

)

dataset.to_csv(

    "dataset/final_dataset.csv",

    index=False,

    encoding="utf-8-sig"

)

# ==========================================================
# STATISTIK
# ==========================================================

print("\n")

print("=" * 60)

print("DATASET BERHASIL DIGABUNGKAN")

print("=" * 60)

print("Jumlah Dataset :", len(dataset))

print()

print(dataset["label"].value_counts())

print()

print("File disimpan : dataset/final_dataset.csv")

print("=" * 60)