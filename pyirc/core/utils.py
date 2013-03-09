def list_items(delimiter, items):
    if len(items) == 0: return ""
    if len(items) == 1: return items[0]
    if len(items) == 2: return "{0} and {1}".format(items[0], items[1])
    return "{0} and {1}".format((delimiter + " ").join(items[:-1]), items[-1])