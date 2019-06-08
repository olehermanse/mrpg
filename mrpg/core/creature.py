from collections import OrderedDict

from mrpg.utils.utils import limit, internal
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
        self.alive = True

    def __str__(self):
        return self.name

    def add_effect(self, effect, source=None):
        self.effects.append(effect)

    def has_effect(self, effect_name):
        effect_name = internal(effect_name)
        for e in self.effects:
            compare = internal(e.name)
            if compare == effect_name:
                return True
        return False

    def modify_effects(self):
        events = []
        for effect in self.effects:
            events += effect.modify() # Modify funcs return events
        return events

    def proc_effects(self):
        events = []
        for effect in self.effects:
            events += effect.proc() # Proc funcs return events
        return events

    def tick_effects(self):
        for effect in self.effects:
            effect.tick() # This just decreases duration counter

    def clean_effects(self):
        names = []
        new_effects = {} # Deduplicate and skip done (expired) effects
        for effect in self.effects:
            name = effect.name
            if effect.is_done():
                # Record name so we can print faded message:
                names.append(name)
                # Don't add to new_effects
            else:
                if (name not in new_effects) or (effect.duration >
                                                 new_effects[name].duration):
                    new_effects[name] = effect

        self.effects = [effect for name, effect in new_effects.items()]
        return names

    def battle_end(self):
        self.effects = []
        self.use_skill = None

    def flee(self):
        self.fleeing = True
        return "{} fled like a big coward.".format(self.name)

    def pick_skill(self, skill):
        assert skill is not None
        self.use_skill = self.skills.equipped.get(skill)
        assert self.use_skill is not None

    def ai(self):
        self.use_skill = self.skills.equipped.get_random()
        assert self.use_skill is not None

    def mitigation(self, amount, type):
        if type == "physical":
            return max(1, amount - self.current["str"])
        if type == "magic":
            return max(1, amount - self.current["int"])
        raise AssertionError

    def damage(self, amount, source=None):
        self.current["hp"] -= amount
        msg = ["{} lost {} hit points".format(self.name, amount)]
        if source:
            msg[0] += " from {}".format(source)
        return msg

    def restore(self, amount, source=None):
        self.current["hp"] += amount
        msg = ["{} restored {} hit points".format(self.name, amount)]
        if source:
            msg[0] += " from {}".format(source)
        return msg

    def reset_stats(self):
        self.current["str"] = self.base["str"]
        self.current["dex"] = self.base["dex"]
        self.current["int"] = self.base["int"]

    def reset_resources(self):
        self.current["hp"] = self.base["hp"]
        self.current["mp"] = self.base["mp"]

    def full_heal(self):
        self.reset_resources()
        self.reset_stats()

    def kill(self):
        self.current["hp"] = 0
        self.alive = False

    def limit_check(self):
        if self.alive and (self.current["hp"] <= 0):
            self.current["hp"] = 0
        if self.current["hp"] > self.base["hp"]:
            self.current["hp"] = self.base["hp"]

        return self.current["hp"] == 0 and self.is_alive()

    def is_alive(self):
        return self.alive

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

    def string_short(self):
        return "Lv.{lvl} {n}".format(n=self.name, lvl=self.level)

    def long_lines(self, skills=False):
        lines = [self.string_short()]
        lines += self.current.get_strings(self.base)
        if skills:
            lines += ["", "Skills:"]
            lines += self.skills.equipped.names()
        return lines

    def string_long(self, skills=False):
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
