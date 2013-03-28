def list_items(delimiter, items):
    if len(items) == 0: return ""
    if len(items) == 1: return items[0]
    if len(items) == 2: return "{0} and {1}".format(items[0], items[1])
    return "{0} and {1}".format((delimiter + " ").join(items[:-1]), items[-1])

def uno_text_color_lookup(color):
    lexicon = {
        None:"white",
        "b":"blue",
        "y":"yellow",
        "g":"green",
        "r":"red"
    }
    return lexicon.get(color,None)

def text_color(text, color, color_converter = lambda i:i):
    lexicon = {
        "white":0,
        "black":1,
        "blue":2,
        "green":3,
        "red":4,
        "brown":5,
        "purple":6,
        "orange":7,
        "yellow":8
    }
    # \x035cam\x03
    return "\x03{0}{1}\x0F".format(lexicon.get(color_converter(color), ""), text)