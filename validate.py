def parse_year(year: str) -> int:
    if year is None or year == '':
        raise ValueError
    value = int(year)
    if value < 0:
        raise ValueError
    return value
