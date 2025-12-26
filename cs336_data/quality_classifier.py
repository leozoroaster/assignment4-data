import gzip
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

GZ_PATH = BASE_DIR.parent / "enwiki-20240420-extracted_urls.txt.gz"

TXT_PATH = BASE_DIR.parent / "enwiki-20240420-extracted_urls.txt"

#with gzip.open(GZ_PATH, "rt", encoding="utf-8") as fin:
    #with open(TXT_PATH, "w", encoding="utf-8") as fout:
        #for line in fin:
            #fout.write(line)

with open(TXT_PATH, "r", encoding="utf-8") as f:
    i=0
    for line in f:
        if i>100:
            break
        i+=1
        print(line)

#no disk space