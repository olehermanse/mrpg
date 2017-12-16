class Creature:
    def __init__(self, name="Not", level=1):
        assert isinstance(level, int)
        self.name  = name
        self.level = level

    def __str__(self):
        return "Lv.{lvl} {n}".format(n=self.name, lvl=self.level)

    def export_data(self):
        d = OrderedDict()
        d["name"] = self.name
        d["level"] = self.level
        s = json.dumps(d, indent=2, ensure_ascii=False)
        return s

    def import_data(self, data):
        if isinstance(data, str):
            data = json_load(data)
        self.name  = data["name"]
        self.level = data["level"]
