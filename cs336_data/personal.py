import re

EMAIL_RE = re.compile(
    r"\b[A-Za-z0-9._%+-]+@(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}\b"
)

PHONE_RE = re.compile(
    r"""
    (?<!\w)
    (?:\+1|1)?
    (?:\(\d{3}\)|\d{3})
    [-.\s]?
    \d{3}
    [-.\s]?
    \d{4}
    (?!\w)
    """,
    re.VERBOSE,
)

IP_RE = re.compile(
    r"\b(?:\d|\d{2}|1\d\d|2[0-4]\d|25[0-5])\.(?:\d|\d{2}|1\d\d|2[0-4]\d|25[0-5])\.(?:\d|\d{2}|1\d\d|2[0-4]\d|25[0-5])\.(?:\d|\d{2}|1\d\d|2[0-4]\d|25[0-5])\b"
)

def mask_email(input_str):
    masked_str, count = re.subn(EMAIL_RE, "|||EMAIL_ADDRESS|||", input_str)
    return masked_str, count

def mask_phone(input_str):
    masked_str, count = re.subn(PHONE_RE, "|||PHONE_NUMBER|||", input_str)
    return masked_str, count

def mask_ip(input_str):
    masked_str, count = re.subn(IP_RE, "|||IP_ADDRESS|||", input_str)
    return masked_str, count