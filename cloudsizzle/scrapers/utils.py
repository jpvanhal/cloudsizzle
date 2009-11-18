import re

def remove_extra_whitespace(text):
    return re.sub('\s+', ' ', text)
    