UNITS = {"h": 60, "m": 1, "s": 1}


def parse_duration(text):
    total = 0
    number = ""
    for char in text:
        if char.isdigit():
            number += char
        else:
            total += int(number) * UNITS[char]
            number = ""
    if number:
        total += int(number)
    return total
