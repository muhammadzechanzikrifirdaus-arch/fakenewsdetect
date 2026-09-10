import os
import joblib
from preprocess_utils import preprocess_text   # <-- IMPORT FUNGSI PREPROCESSING!

# ======================================================
# LOAD MODEL
# ======================================================

MODEL_PATH = "model/model.pkl"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        "Model tidak ditemukan. Jalankan train.py terlebih dahulu."
    )

model = joblib.load(MODEL_PATH)

# ======================================================
# PREDICT FUNCTION
# ======================================================

def predict_news(text):
    text = str(text).strip()

    if len(text) == 0:
        return {
            "label": "UNKNOWN",
            "confidence": 0,
            "hoax_probability": 0,
            "valid_probability": 0
        }

    # Preprocess teks dulu sebelum prediksi
    processed_text = preprocess_text(text)

    # Prediksi pakai teks yang sudah diproses
    prediction = model.predict([processed_text])[0]

    # Probabilitas
    probability = model.predict_proba([processed_text])[0]

    hoax_probability = round(float(probability[0]) * 100, 2)
    valid_probability = round(float(probability[1]) * 100, 2)

    confidence = round(max(
        hoax_probability,
        valid_probability
    ), 2)

    if prediction == 1:
        label = "VALID"
    else:
        label = "HOAX"

    return {
        "label": label,
        "confidence": confidence,
        "hoax_probability": hoax_probability,
        "valid_probability": valid_probability
    }

# ======================================================
# TEST MANUAL
# ======================================================

if __name__ == "__main__":
    print("=" * 55)
    print("       INDONESIAN FAKE NEWS DETECTION AI")
    print("=" * 55)

    while True:
        berita = input("\nMasukkan berita ('exit' untuk keluar):\n> ")

        if berita.lower() == "exit":
            break

        hasil = predict_news(berita)

        print("\n" + "=" * 55)
        print("HASIL ANALISIS")
        print("=" * 55)

        print(f"Prediksi            : {hasil['label']}")
        print(f"Confidence          : {hasil['confidence']}%")
        print(f"Probabilitas HOAX   : {hasil['hoax_probability']}%")
        print(f"Probabilitas VALID  : {hasil['valid_probability']}%")

        print("=" * 55)