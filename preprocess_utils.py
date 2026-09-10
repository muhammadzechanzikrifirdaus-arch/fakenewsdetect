import re
import string
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Inisialisasi sekali di awal (biar gak di-load tiap prediksi)
stop_factory = StopWordRemoverFactory()
stopwords = stop_factory.get_stop_words()
stemmer = StemmerFactory().create_stemmer()

def preprocess_text(text):
    """Fungsi preprocessing teks: case folding, hapus URL, angka, tanda baca, stopword, stemming"""
    text = str(text).lower()
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"www\S+", " ", text)
    text = re.sub(r"\d+", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text)
    
    hasil = []
    for word in text.split():
        if word not in stopwords:
            hasil.append(stemmer.stem(word))
    
    return " ".join(hasil)