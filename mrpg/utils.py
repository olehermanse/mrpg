from collections import OrderedDict

def limit(x, low, high):
    if x < low:
        return low
    if x > high:
        return high
    return x

class CustomDict:
    def __init__(self):
        self.d = OrderedDict()

    def __getitem__(self, key):
        return self.d[key]

    def __setitem__(self, key, value):
        self.d[key] = value

    def __contains__(self, key):
        if key in self.d:
            return True
        return False

def column_lines(*args):
    row_count = 1
    for arg in args:
        if type(arg) is list and len(arg) > row_count:
            row_count = len(arg)
    args = map(lambda x: [x] * row_count if type(x) is str else x, args)
    zipped = zip(*args)
    rows = list(zipped)
    rows = [[str(cell) for cell in row] for row in rows]
    columns = list(zip(*rows))
    widths = [max(map(len,col)) for col in columns]
    lines = []
    for row in rows:
        line = []
        for index, element in enumerate(row):
            line.append(element.ljust(widths[index], " "))
        lines.append("".join(line))
    return lines

def column_string(*args):
    lines = column_lines(*args)
    return "\n".join(lines)
