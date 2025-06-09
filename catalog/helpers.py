from django.utils.text import slugify
from secrets import token_hex


def my_slugify(text):
    return f"{slugify(text)}-{token_hex(2)}"
