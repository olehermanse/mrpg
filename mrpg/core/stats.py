from mrpg.utils.utils import CustomDict
from mrpg.utils.utils import column_lines


class Stats(CustomDict):
    def __init__(self, level=0):
        super().__init__()
        self.set_level(level)

    def get_strings(self, compare=None):
        keys = list(filter(lambda x: x != "name" and x != "level", self))
        values = []
        for key in keys:
            if compare and key in compare:
                values.append("{}/{}".format(self[key], compare[key]))
            else:
                values.append(str(self[key]))
        lines = column_lines(keys, " = ", values)
        return lines

    def set_level(self, level):
        assert type(level) is int
        assert level >= 0
        self["hp"] = level * 2 + (8 if level > 0 else 0)
        self["mp"] = level * 2 + (8 if level > 0 else 0)
        self["str"] = level + (2 if level > 0 else 0)
        self["dex"] = level + (2 if level > 0 else 0)
        self["int"] = level + (2 if level > 0 else 0)

    def copy_from(self, source):
        for key in self:
            self[key] = source[key]
