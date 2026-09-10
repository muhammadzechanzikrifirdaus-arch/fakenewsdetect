import os
import joblib
import pandas as pd

from preprocess_utils import preprocess_text   # <-- IMPORT DARI UTILS

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# =====================================================
# LOAD DATASET
# =====================================================

print("=" * 60)
print("FAKE NEWS DETECTION AI")
print("=" * 60)

print("\n[1/6] Loading dataset...")

df = pd.read_csv("dataset/final_dataset.csv")

print(f"Total dataset : {len(df)}")

# =====================================================
# CLEAN DATA
# =====================================================

print("\n[2/6] Cleaning dataset...")

df.dropna(inplace=True)
df.drop_duplicates(inplace=True)
df = df[df["text"].str.len() > 20]
df.reset_index(drop=True, inplace=True)

print("Dataset bersih :", len(df))

# =====================================================
# PREPROCESSING (PAKAI DARI preprocess_utils.py)
# =====================================================

print("\n[3/6] Preprocessing...")

df["text"] = df["text"].apply(preprocess_text)   # <-- PAKAI FUNGSI YANG SAMA

print("Preprocessing selesai.")

# =====================================================
# SPLIT DATA
# =====================================================

print("\n[4/6] Split dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    df["text"],
    df["label"],
    test_size=0.2,
    random_state=42,
    stratify=df["label"]
)

print("Training :", len(X_train))
print("Testing  :", len(X_test))

# =====================================================
# MACHINE LEARNING
# =====================================================

print("\n[5/6] Training Naive Bayes...")

model = Pipeline([
    ("tfidf", TfidfVectorizer(
        max_features=10000,
        ngram_range=(1,2)
    )),
    ("nb", MultinomialNB(
        alpha=0.5,
        fit_prior=False
    ))
])

model.fit(X_train, y_train)

print("Training selesai.")

# =====================================================
# EVALUASI
# =====================================================

print("\n[6/6] Evaluasi model...")

pred = model.predict(X_test)

accuracy = accuracy_score(y_test, pred)

print()
print("=" * 60)
print("Accuracy")
print("=" * 60)
print(f"{accuracy*100:.2f}%")

print()
print("=" * 60)
print("Classification Report")
print("=" * 60)
print(classification_report(y_test, pred))

print()
print("=" * 60)
print("Confusion Matrix")
print("=" * 60)
print(confusion_matrix(y_test, pred))

# =====================================================
# SAVE MODEL
# =====================================================

print()
print("Menyimpan model...")

os.makedirs("model", exist_ok=True)

joblib.dump(model, "model/model.pkl")

print()
print("=" * 60)
print("MODEL BERHASIL DISIMPAN")
print("=" * 60)
print("Lokasi : model/model.pkl")
print("=" * 60)