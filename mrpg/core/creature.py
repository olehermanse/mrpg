from collections import OrderedDict
from mrpg.platform.files import jsonify
from mrpg.core.funcs import column_lines
from mrpg.core.skills import Skills

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
        lines = column_lines(keys, " = ", values)
        return lines

    def set_level(self, level):
        assert type(level) is int
        assert level >= 0
        self["hp"]  = level * 2 + (10 if level > 0 else 0)
        self["mp"]  = level * 2 + (10 if level > 0 else 0)
        self["str"] = level + (5 if level > 0 else 0)
        self["dex"] = level + (5 if level > 0 else 0)
        self["int"] = level + (5 if level > 0 else 0)

    def copy_from(self, source):
        for key in self.d:
            self[key] = source[key]

class Creature:
    def __init__(self, name="Not", level=1):
        assert isinstance(level, int)
        self.init(name, level)

    def init(self, name, level):
        self.name = name
        self.base = Stats(level)
        self.current = Stats(level)
        self.set_level(level)
        self.skills = [Skills.get("attack"), Skills.get("heal")]
        self.use_skill = None

    def get_skill(self, name):
        matches = list(filter(lambda x: x.name == name, self.skills))
        assert len(matches) == 1
        return matches[0]

    def get_skill_names(self):
        return list(map(lambda x: x.name, self.skills))

    def damage(self, amount):
        self.current["hp"] -= amount
        return ["{} lost {} hit points".format(self.name, amount)]

    def restore(self, amount):
        self.current["hp"] += amount
        return ["{} restored {} hit points".format(self.name, amount)]

    def limit_check(self):
        if self.current["hp"] <= 0:
            self.current["hp"] = 0
            return ["{} died".format(self.name)]
        if self.current["hp"] > self.base.hp:
            self.current["hp"] = self.base.hp
            return ["{} was fully healed".format(self.name)]
        return []

    def set_level(self, level):
        self.level = level
        self.base.set_level(level)
        self.current.set_level(level)

    def __str__(self):
        return self.string_short()

    def string_short(self):
        return "Lv.{lvl} {n}".format(n=self.name, lvl=self.level)

    def long_lines(self):
        lines = [self.string_short()]
        lines += self.current.get_strings(self.base)
        return lines

    def string_long(self):
        lines = self.long_lines()
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
