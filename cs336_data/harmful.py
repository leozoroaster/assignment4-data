from pathlib import Path
import fasttext
import numpy as np
import re

BASE_DIR = Path(__file__).resolve().parent

NSFW_PATH = BASE_DIR.parent / "jigsaw_fasttext_bigrams_nsfw_final.bin"

HATE_PATH = BASE_DIR.parent / "jigsaw_fasttext_bigrams_hatespeech_final.bin"

model_nsfw=fasttext.load_model(str(NSFW_PATH))

model_hate=fasttext.load_model(str(HATE_PATH))

def is_nsfw(unicode_str):
    #clean text
    text = re.sub(r"\s+", " ", unicode_str).strip()

    labels, probs = model_nsfw.predict(text, k=3)
    result=labels[0].replace("__label__", "")

    confidence = probs[0]
    if confidence>=1:
        confidence=1.0
    if confidence<=0:
        confidence=0.0

    return result, confidence

def is_hate(unicode_str):
    #clean text
    text = re.sub(r"\s+", " ", unicode_str).strip()

    labels, probs = model_hate.predict(text, k=3)
    result=labels[0].replace("__label__", "")

    confidence = probs[0]
    if confidence>=1:
        confidence=1.0
    if confidence<=0:
        confidence=0.0

    return result, confidence
