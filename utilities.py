import re

def capitalize_first_letter(s):
    if not s:
        return s
    return s[0].upper() + s[1:].lower()

def clean_number(phone_num):
    return ''.join(filter(str.isdigit, phone_num))

def is_valid_phone_number(phone_num):
    pattern = re.compile(r'^(?:\d{3}[-. ]?)?\d{3}[-. ]?\d{4}$')
    return bool(pattern.match(phone_num))
