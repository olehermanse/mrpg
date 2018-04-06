from collections import OrderedDict

from mrpg.platform.files import jsonify, json_load
from mrpg.utils import limit
from mrpg.core.skills import Skills, CreatureSkillCollection
from mrpg.core.stats import Stats


class Creature:
    def __init__(self, name="Not", level=1, skill_names=None):
        assert isinstance(level, int)
        self.init(name, level, skill_names)

    def init(self, name, level, skill_names=None):
        self.name = name
        self.base = Stats(level)
        self.current = Stats(level)
        self.set_level(level)
        self.exp = 0
        self.skills = CreatureSkillCollection(skill_names)
        self.use_skill = None

    def damage(self, amount, limit_check=False):
        self.current["hp"] -= amount
        msg = ["{} lost {} hit points".format(self.name, amount)]
        if limit_check:
            msg.append(self.limit_check())
        return msg

    def restore(self, amount, limit_check=False):
        self.current["hp"] += amount
        msg = ["{} restored {} hit points".format(self.name, amount)]
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
        lines += self.skills.equipped.names()
        return lines

    def string_long(self):
        lines = self.long_lines()
        s = "\n".join(lines)
        return s

    def export_data(self):
        d = OrderedDict()
        d["name"] = self.name
        d["level"] = self.level
        d["skills"] = self.skills.export_data()
        return d

    def import_data(self, data):
        self.name = data["name"]
        self.set_level(data["level"])
        self.skills.import_data(data["skills"])
