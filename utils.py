def int_parse(str):
    try:
        return int(str)
    except ValueError:
        if str == 'A':
            return 14
        elif str == 'K':
            return 13
        elif str == 'Q':
            return 12
        elif str == 'J':
            return 11
        else:
            return None
