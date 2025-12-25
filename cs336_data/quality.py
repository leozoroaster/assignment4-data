import nltk
nltk.download("punkt")
nltk.download("punkt_tab")
from nltk.tokenize import word_tokenize

example_text = "Hello, world! This is NLTK's word tokenizer."
example_tokens = word_tokenize(example_text)
print(example_tokens)

def check_word_count(tokens):
    length=len(tokens)
    return length>=50 and length<=100000

def check_mean_word_length(tokens):
    length = len(tokens)
    word_length=sum([len(token) for token in tokens])
    return length>=1 and word_length/length>=3 and word_length/length<=10

def contain_ellipsis(line):
    return line.rstrip().endswith("...")

def ellipsis_count(text):
    lines = [line for line in text.splitlines() if line.strip()]
    length = len(lines)
    ellipsis_count = sum([contain_ellipsis(line) for line in lines])
    return length >= 1 and ellipsis_count / length <=0.3

def contain_ab(token):
    for char in token:
        if char.isalpha():
            return 1
    return 0

def ab_count(tokens):
    length = len(tokens)
    ab_count = sum([contain_ab(token) for token in tokens])
    return length >= 1 and ab_count / length >= 0.8

def quality_check(text):
    tokens=word_tokenize(text)
    return check_word_count(tokens) and check_mean_word_length(tokens) and ellipsis_count(text) and ab_count(tokens)

