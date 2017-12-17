from collections import OrderedDict
from mrpg.platform.files import jsonify

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

class Creature:
    def __init__(self, name="Not", level=1):
        assert isinstance(level, int)
        self.d = OrderedDict()
        self.d["name"]  = name
        self.set_level(level)

    def set_level(self, level):
        self.d["level"] = level
        self.d["hp"]    = 10 + level * 2
        self.d["mp"]    = 10 + level * 2
        self.d["str"]   = 5 + level
        self.d["dex"]   = 5 + level
        self.d["int"]   = 5 + level

    def __str__(self):
        return self.string_short()

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        return self.d[name]

    def string_short(self):
        return "Lv.{lvl} {n}".format(n=self.name, lvl=self.level)

    def string_long(self):
        lines = [self.string_short()]
        keys = list(filter(lambda x: x!="name" and x!="level", self.d))
        values = [self.d[x] for x in keys]
        lines += column_string(keys, "=", values)
        s = "\n".join(lines)
        return s

    def export_data(self):
        d = OrderedDict()
        d["name"] = self.name
        d["level"] = self.level
        s = jsonify(d)
        return s

    def import_data(self, data):
        if isinstance(data, str):
            data = json_load(data)
        self.name  = data["name"]
        self.set_level(data["level"])
