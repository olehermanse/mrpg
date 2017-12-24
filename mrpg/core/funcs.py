def column_string(*args):
    row_count = len(args[0])
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
        lines.append(" ".join(line))
    return lines
