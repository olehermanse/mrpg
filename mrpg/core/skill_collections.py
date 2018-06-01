import random

from collections import OrderedDict

from mrpg.core.skills import Skills


class SkillCollection:
    def __init__(self, add_skills=None):
        self.skills = []
        if add_skills is not None:
            for s in add_skills:
                self.add(s)

    def index(self, skill):
        if skill in self.skills:
            return self.skills.index(skill)
        if type(skill) is str:
            for s in self.skills:
                if s.name.lower() == skill.lower():
                    return self.skills.index(s)
        return None

    def __contains__(self, skill):
        index = self.index(skill)
        return True if index is not None else False

    def get(self, name):
        if type(name) is int:
            return self.skills[name]
        index = self.index(name)
        return None if index is None else self.skills[index]

    def get_random(self):
        return random.choice(self.skills)

    def add(self, skill):
        if isinstance(skill, list):
            for i in skill:
                self.add(i)
            return
        assert skill not in self.skills
        skill = Skills.get(skill)
        assert skill not in self.skills
        self.skills.append(skill)

    def remove(self, skill):
        assert skill in self.skills
        index = self.index(skill)
        assert index >= 0
        del self.skills[index]

    def names(self):
        return [x.name for x in self.skills]

    def hints(self):
        return [x.hint for x in self.skills]


class CreatureSkillCollection:
    def __init__(self, add_skills=None):
        self.learned = SkillCollection(add_skills)
        self.equipped = SkillCollection(add_skills)

    def has_learned(self, skill):
        return skill in self.learned

    def has_equipped(self, skill):
        return skill in self.equipped

    def learn(self, skill):
        self.learned.add(skill)

    def unlearn(self, skill):
        self.learned.remove(skill)

    def equip(self, skill):
        self.equipped.add(skill)

    def unequip(self, skill):
        self.equipped.remove(skill)

    def export_data(self):
        d = OrderedDict()
        d["equipped"] = self.equipped.names()
        d["learned"] = self.learned.names()
        return d

    def import_data(self, d):
        equipped, learned = d["equipped"], d["learned"]
        for s in equipped:
            self.equip(s)
        for s in learned:
            self.learn(s)
