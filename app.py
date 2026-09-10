from flask import Flask, render_template, request, jsonify
from predict import predict_news

import subprocess
import pandas as pd
import os
import sys
import time

app = Flask(__name__)

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

    return jsonify({

        "status": "running",

        "model_exist": os.path.exists("model/model.pkl"),

        "dataset_exist": os.path.exists("dataset/final_dataset.csv")

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

    if not os.path.exists("dataset/final_dataset.csv"):

        return jsonify({

            "total": 0,

            "valid": 0,

            "hoax": 0

        })

    df = pd.read_csv(

        "dataset/final_dataset.csv"

    )

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

    exist = os.path.exists(

        "dataset/final_dataset.csv"

    )

    total = 0

    if exist:

        df = pd.read_csv(

            "dataset/final_dataset.csv"

        )

        total = len(df)

    return jsonify({

        "exist": exist,

        "total": total

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