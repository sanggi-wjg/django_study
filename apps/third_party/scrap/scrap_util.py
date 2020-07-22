def escape_number(text):
    text = text.replace(',', '')
    text = text.replace('+', '')
    text = text.replace('--', '-')
    return text


def escape_char(text):
    text = text.replace('%', '')
    return text
