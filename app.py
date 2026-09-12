from flask import Flask, render_template, request, jsonify
from predict import predict_news

import subprocess
import pandas as pd
import os
import sys
import time

app = Flask(__name__)

# ==========================================================
# DATASET
# ==========================================================

DATASET_URL = "https://etiifvbxqwjyty8l.private.blob.vercel-storage.com/dataset/final_dataset.csv?vercel-blob-valid-until=1789179094046&vercel-blob-delegation=eyJzdG9yZUlkIjoic3RvcmVfZXRJaUZWYnhxV2pZVHk4TCIsIm93bmVySWQiOiJ0ZWFtX3F1c3ZwWWswWlpSbjZHc1JDeVdWdElzRyIsInBhdGhuYW1lIjoiKiIsIm9wZXJhdGlvbnMiOlsiZ2V0IiwiaGVhZCJdLCJ2YWxpZFVudGlsIjoxNzg5MjIyMDg2Mjg2LCJpYXQiOjE3ODkxNzg4ODY3MDd9.sbE83m64zLQSW1yasIIlAQl7_8-sLsdT5ql2sENBrYc&vercel-blob-signature=iWalasMnU1ihZkIhTDmPpTeWS0TxZCReGc_4G0CXxdM"


# ==========================================================
# HOME
# ==========================================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================================
# PREDICT
# ==========================================================

@app.route("/predict", methods=["POST"])
def predict():

    if not os.path.exists("model/model.pkl"):

        return jsonify({
            "success": False,
            "message": "Model belum tersedia. Silakan lakukan training terlebih dahulu."
        })

    data = request.get_json()

    title = data.get("title", "")
    content = data.get("content", "")

    text = (title + " " + content).strip()

    if len(text) == 0:

        return jsonify({
            "success": False,
            "message": "Masukkan judul atau isi berita."
        })

    start = time.time()

    result = predict_news(text)

    elapsed = round(time.time() - start, 3)

    return jsonify({

        "success": True,

        "prediction": result["label"],

        "confidence": result["confidence"],

        "hoax_probability": result["hoax_probability"],

        "valid_probability": result["valid_probability"],

        "processing_time": elapsed

    })


# ==========================================================
# STATUS
# ==========================================================

@app.route("/status")
def status():

    try:

        dataset_exist = False

        try:
            pd.read_csv(
                DATASET_URL,
                nrows=1
            )

            dataset_exist = True

        except Exception:
            dataset_exist = False

        return jsonify({

            "status": "running",

            "model_exist": os.path.exists("model/model.pkl"),

            "dataset_exist": dataset_exist

        })

    except Exception as e:

        return jsonify({

            "status": "running",

            "model_exist": os.path.exists("model/model.pkl"),

            "dataset_exist": False,

            "error": str(e)

        })


# ==========================================================
# MODEL INFO
# ==========================================================

@app.route("/model-info")
def model_info():

    info = {

        "algorithm": "Multinomial Naive Bayes",

        "vectorizer": "TF-IDF",

        "language": "Bahasa Indonesia",

        "dataset": "final_dataset.csv"

    }

    if os.path.exists("model/model.pkl"):

        info["model_size"] = round(

            os.path.getsize("model/model.pkl") / 1024,

            2

        )

    else:

        info["model_size"] = 0

    return jsonify(info)


# ==========================================================
# DATASET INFO
# ==========================================================

@app.route("/dataset-info")
def dataset_info():

    try:

        df = pd.read_csv(DATASET_URL)

        total = len(df)

        valid = int(
            (df["label"] == 1).sum()
        )

        hoax = int(
            (df["label"] == 0).sum()
        )

        return jsonify({

            "total": total,

            "valid": valid,

            "hoax": hoax

        })

    except Exception as e:

        return jsonify({

            "total": 0,

            "valid": 0,

            "hoax": 0,

            "error": str(e)

        })


# ==========================================================
# UPDATE DATASET (SCRAPING)
# ==========================================================

@app.route("/update-dataset", methods=["POST"])
def update_dataset():

    try:

        logs = []

        start = time.time()

        # ---------------- RSS ----------------

        subprocess.run(

            [sys.executable, "scraper_rss.py"],

            check=True

        )

        logs.append("✓ RSS berhasil diperbarui")

        # ---------------- GNEWS ----------------

        subprocess.run(

            [sys.executable, "scraper_gnews.py"],

            check=True

        )

        logs.append("✓ GNews berhasil diperbarui")

        # ---------------- NEWSDATA ----------------

        subprocess.run(

            [sys.executable, "scraper_newsdata.py"],

            check=True

        )

        logs.append("✓ NewsData berhasil diperbarui")

        # ---------------- MERGE ----------------

        subprocess.run(

            [sys.executable, "merge_dataset.py"],

            check=True

        )

        logs.append("✓ Dataset berhasil digabung")

        elapsed = round(

            time.time() - start,

            2

        )

        return jsonify({

            "success": True,

            "message": "Dataset berhasil diperbarui.",

            "logs": logs,

            "time": elapsed

        })

    except subprocess.CalledProcessError as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })


# ==========================================================
# RETRAIN MODEL
# ==========================================================

@app.route("/retrain", methods=["POST"])
def retrain():

    try:

        start = time.time()

        subprocess.run(

            [sys.executable, "train.py"],

            check=True

        )

        elapsed = round(

            time.time() - start,

            2

        )

        return jsonify({

            "success": True,

            "message": "Model berhasil dilatih ulang.",

            "training_time": elapsed

        })

    except subprocess.CalledProcessError as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })


# ==========================================================
# CHECK MODEL
# ==========================================================

@app.route("/check-model")
def check_model():

    exist = os.path.exists(
        "model/model.pkl"
    )

    size = 0

    if exist:

        size = round(

            os.path.getsize("model/model.pkl") / 1024,

            2

        )

    return jsonify({

        "exist": exist,

        "size": size

    })


# ==========================================================
# CHECK DATASET
# ==========================================================

@app.route("/check-dataset")
def check_dataset():

    try:

        df = pd.read_csv(
            DATASET_URL
        )

        total = len(df)

        return jsonify({

            "exist": True,

            "total": total

        })

    except Exception as e:

        return jsonify({

            "exist": False,

            "total": 0,

            "error": str(e)

        })


# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.route("/health")
def health():

    return jsonify({

        "status": "OK",

        "server": "Running",

        "time": time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    })


# ==========================================================
# RUN APP
# ==========================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )
