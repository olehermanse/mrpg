from collections import OrderedDict

from mrpg.utils import CustomDict

from mrpg.platform.files import jsonify, json_load
from mrpg.utils import column_lines, limit
from mrpg.core.skills import Skills
from mrpg.core.stats import Stats

class Creature:
    def __init__(self, name="Not", level=1):
        assert isinstance(level, int)
        self.init(name, level)

    def init(self, name, level):
        self.name = name
        self.base = Stats(level)
        self.current = Stats(level)
        self.set_level(level)
        self.exp = 0
        skill_names = ["attack"]
        self.set_skills(skill_names)
        self.use_skill = None

    def set_skills(self, skill_names):
        self.skill_names = skill_names
        self.skills = [Skills.get(x) for x in skill_names]

    def get_skill(self, name):
        matches = list(filter(lambda x: x.name == name, self.skills))
        assert len(matches) == 1
        return matches[0]

    def get_skill_names(self):
        return list(map(lambda x: x.name, self.skills))

    def get_skill_hints(self):
        return list(map(lambda x: x.hint, self.skills))

    def damage(self, amount, limit_check=False):
        self.current["hp"] -= amount
        msg =  ["{} lost {} hit points".format(self.name, amount)]
        if limit_check:
            msg.append(self.limit_check())
        return msg

    def restore(self, amount, limit_check=False):
        self.current["hp"] += amount
        msg =  ["{} restored {} hit points".format(self.name, amount)]
        if limit_check:
            msg.append(self.limit_check())
        return msg

    def limit_check(self):
        if self.current["hp"] <= 0:
            self.current["hp"] = 0
            return ["{} died".format(self.name)]
        if self.current["hp"] > self.base["hp"]:
            self.current["hp"] = self.base["hp"]
            return ["{} was fully healed".format(self.name)]
        return []

    def is_alive(self):
        hp = self.current["hp"]
        assert hp >= 0
        return hp > 0

    def set_level(self, level):
        self.level = level
        self.base.set_level(level)
        self.current.set_level(level)

    def exp_reward(self):
        return (3 * self.level) // 2

    def max_exp(self):
        return self.exp_reward() * limit(self.level, 1, 8)

    def gain_exp(self, exp):
        msg = ["{} gained {} experience points".format(self.name, exp)]
        self.exp += exp
        max_exp = self.max_exp()
        if self.exp >= max_exp:
            self.exp -= max_exp
            self.set_level(self.level + 1)
            msg.append("{} leveled up".format(self.name))
        return msg

    def __str__(self):
        return self.string_short()

    def string_short(self):
        return "Lv.{lvl} {n}".format(n=self.name, lvl=self.level)

    def long_lines(self):
        lines = [self.string_short()]
        lines += self.current.get_strings(self.base)
        lines += ["", "Skills:"]
        lines += self.skill_names
        return lines

    def string_long(self):
        lines = self.long_lines()
        s = "\n".join(lines)
        return s

    def export_data(self):
        d = OrderedDict()
        d["name"] = self.name
        d["level"] = self.level
        d["skills"] = self.skill_names
        s = jsonify(d)
        return s

    def import_data(self, data):
        if isinstance(data, str):
            data = json_load(data)
        self.name  = data["name"]
        self.set_level(data["level"])
        self.set_skills(data["skills"])
