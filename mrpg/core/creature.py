from collections import OrderedDict
from mrpg.platform.files import jsonify
from mrpg.core.funcs import column_string

class CustomDict:
    def __init__(self):
        self.d = OrderedDict()

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        return self.d[name]

    def __getitem__(self, key):
        return self.d[key]

    def __setitem__(self, key, value):
        self.d[key] = value

class Stats(CustomDict):
    def __init__(self, level=0):
        super().__init__()
        self.set_level(level)

    def get_strings(self, compare=None):
        keys = list(filter(lambda x: x!="name" and x!="level", self.d))
        values = []
        for key in keys:
            if compare and key in compare.d:
                values.append("{}/{}".format(self.d[key], compare.d[key]))
            else:
                values.append(str(self.d[key]))
        lines = column_string(keys, "=", values)
        return lines

    def set_level(self, level):
        assert type(level) is int
        assert level >= 0
        self.d["hp"]  = level * 2 + (10 if level > 0 else 0)
        self.d["mp"]  = level * 2 + (10 if level > 0 else 0)
        self.d["str"] = level + (5 if level > 0 else 0)
        self.d["dex"] = level + (5 if level > 0 else 0)
        self.d["int"] = level + (5 if level > 0 else 0)

    def copy_from(self, source):
        for key in self.d:
            self[key] = source[key]

class Creature(CustomDict):
    def __init__(self, name="Not", level=1):
        assert isinstance(level, int)
        self.d = OrderedDict()
        self.name = name
        self.level = level
        self.base = Stats(level)
        self.current = Stats(level)
        self.skills = []
        self.skill_pick = None

    def set_level(self, level):
        self.base.set_level(level)
        self.current.set_level(level)

    def __str__(self):
        return self.string_short()

    def string_short(self):
        return "Lv.{lvl} {n}".format(n=self.name, lvl=self.level)

    def string_long(self):
        lines = [self.string_short()]
        lines += self.current.get_strings(self.current)
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
