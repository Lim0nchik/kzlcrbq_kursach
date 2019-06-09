def invalid_int(number):
    if not number:
        raise ValueError
    res = int(number)
    if res < 0:
        raise ValueError
    return res


def invalid_float(number):
    if not number:
        raise ValueError
    return float(number)


def invalid_text(text: str):
    if "," in text:
        raise ValueError
    return text.strip()
