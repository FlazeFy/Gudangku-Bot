
def convert_price_number(n):
    in_str = str(n)
    out = ""

    for i, r in enumerate(in_str):
        if i > 0 and (len(in_str) - i) % 3 == 0:
            out += "."
        out += r

    return out
