import json

from collections import OrderedDict

class ExitException(BaseException):
    pass

def printable(name):
    return name[0].upper() + name[1:].lower().replace("_", " ")


def internal(name):
    return name.lower().replace(" ", "_").replace("'", "")


def jsonify(data):
    return json.dumps(data, indent=2, ensure_ascii=False)


def single_newline(lst):
    if len(lst) > 0 and lst[-1] != "":
        lst.append("")
    return lst


def flatten_strings(strings):
    if strings is None:
        return []
    if type(strings) is str:
        return [strings]
    assert type(strings) is list

    new_list = []
    for element in strings:
        expanded = flatten_strings(element)
        for string in expanded:
            new_list.append(string)
    for s in new_list:
        assert type(s) is str
    return new_list


def limit(x, low, high):
    if x < low:
        return low
    if x > high:
        return high
    return x


class CustomDict(OrderedDict):
    pass


def column_lines(*args):
    row_count = 1
    for arg in args:
        if type(arg) is list and len(arg) > row_count:
            row_count = len(arg)
    args = list(map(lambda x: [x] * row_count if type(x) is str else x, args))
    for l in args:
        while len(l) < row_count:
            l.append("")
    zipped = zip(*args)
    rows = list(zipped)
    rows = [[str(cell) for cell in row] for row in rows]
    columns = list(zip(*rows))
    widths = [max(map(len, col)) for col in columns]
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
