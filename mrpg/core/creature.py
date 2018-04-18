from collections import OrderedDict

from mrpg.utils.utils import limit
from mrpg.core.skill_collections import CreatureSkillCollection
from mrpg.core.stats import Stats


class Creature:
    def __init__(self, name="Not", level=1, skill_names=None):
        assert isinstance(level, int)
        self.init(name, level, skill_names)

    def init(self, name, level, skill_names=None):
        self.fleeing = False
        self.name = name
        self.base = Stats(level)
        self.current = Stats(level)
        self.set_level(level)
        self.exp = 0
        self.skills = CreatureSkillCollection(skill_names)
        self.use_skill = None
        self.effects = []

    def add_effect(self, effect, source=None):
        self.effects.append(effect)
        msg = "{} applied {} to {}".format(source, effect.name, self.name)
        return [effect.message or msg]

    def calculate_effects(self):
        return [effect.calculate() for effect in self.effects]

    def apply_effects(self):
        return [effect.apply() for effect in self.effects]

    def tick_effects(self):
        return [effect.tick() for effect in self.effects]

    def clean_effects(self):
        messages = []
        new_effects = []
        for effect in self.effects:
            if effect.is_done():
                messages.append(
                    "{}'s {} faded".format(self.name, effect.name))
            else:
                new_effects.append(effect)

        self.effects = new_effects
        return messages

    def flee(self):
        self.fleeing = True
        return "{} fled like a big coward.".format(self.name)

    def pick_skill(self, skill):
        assert skill is not None
        self.use_skill = self.skills.equipped.get(skill)
        assert self.use_skill is not None

    def damage(self, amount, limit_check=False, source=None):
        self.current["hp"] -= amount
        msg = ["{} lost {} hit points".format(self.name, amount)]
        if source:
            msg[0] += " from {}".format(source)
        if limit_check:
            msg.append(self.limit_check())
        return msg

    def restore(self, amount, limit_check=False, source=None):
        self.current["hp"] += amount
        msg = ["{} restored {} hit points".format(self.name, amount)]
        if source:
            msg[0] += " from {}".format(source)
        if limit_check:
            msg.append(self.limit_check())
        return msg

    def town_heal(self):
        self.current["hp"] = self.base["hp"]

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

    def is_dead(self):
        return not self.is_alive()

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

    def long_lines(self, skills=True):
        lines = [self.string_short()]
        lines += self.current.get_strings(self.base)
        if skills:
            lines += ["", "Skills:"]
            lines += self.skills.equipped.names()
        return lines

    def string_long(self, skills=True):
        lines = self.long_lines(skills)
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
