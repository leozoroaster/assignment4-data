import resiliparse
from resiliparse.extract.html2text import extract_plain_text
from pathlib import Path
import gzip

def extract_text(byte_str):
    str_type=resiliparse.parse.encoding.detect_encoding(byte_str)
    unicode_str=byte_str.decode(str_type, errors="replace")
    return extract_plain_text(unicode_str)

example = b'\xe4\xb8\xad\xe6\x96\x87'

print(extract_text(example))

BASE_DIR = Path(__file__).resolve().parent

WARC_PATH = BASE_DIR.parent / "example.warc.gz"

WET_PATH=BASE_DIR.parent / "example.warc.wet.gz"

print("WARC example")

with gzip.open(WARC_PATH, "rb") as f:
    for i, line in enumerate(f):
        if i >= 100:
            break
        # line is bytes
        print(extract_text(line))
    #warc_bytes = f.read()

print("WET example")

with gzip.open(WET_PATH, "rb") as f:
    for i, line in enumerate(f):
        if i >= 100:
            break
        # line is bytes
        print(extract_text(line))
    #warc_bytes = f.read()
