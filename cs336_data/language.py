from pathlib import Path
import fasttext
import numpy as np
import re

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR.parent / "lid.176.bin"

model=fasttext.load_model(str(MODEL_PATH))

def language_identification(unicode_str):
    #clean text
    text = re.sub(r"\s+", " ", unicode_str).strip()

    labels, probs = model.predict(text, k=3)
    language=labels[0].replace("__label__", "")

    confidence = probs[0]
    if confidence>=1:
        confidence=1.0
    if confidence<=0:
        confidence=0.0

    return language, confidence
