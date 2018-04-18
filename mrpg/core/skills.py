from mrpg.utils.utils import printable, internal
from mrpg.core.effects import Effects
from mrpg.core.applier import Applier


class Skill(Applier):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def apply(self):
        msg = ["{} used {}".format(self.source.name, self.name)]
        return msg + super().apply()


class SkillFuncs:
    def attack():
        obj = Skill(hint="Physical attack")

        def calculate(skill, user, target):
            usr, tar = user.current, target.current
            damage = 2 * usr["str"]
            damage -= tar["str"]
            damage = max([damage, 1])
            skill.power = damage

        def apply(skill, user, target):
            return target.damage(skill.power)

        obj.steps(calculate, apply)

        return obj

    def fireball():
        obj = Skill(hint="Hot magic")

        def calculate(skill, user, target):
            usr, tar = user.current, target.current
            damage = 2 * usr["int"]
            damage -= tar["int"]
            damage = max([damage, 1])
            skill.power = damage

        def apply(skill, user, target):
            ret = []
            ret += target.damage(skill.power)
            burn = Effects.get("burn")
            burn.setup(skill, target)
            burn.message = "{} was burned".format(target.name)
            ret += target.add_effect(burn, source=skill.name)
            return ret

        obj.steps(calculate, apply)

        return obj

    def life_drain():
        obj = Skill(hint="Damage and restore")

        def calculate(skill, user, target):
            usr, tar = user.current, target.current
            amount = 3 * usr["int"] // 2
            amount -= tar["int"]
            amount = max([amount, 2])
            amount = min([amount, user.base["hp"]])
            skill.power = amount

        def apply(skill, user, target):
            messages = []
            messages += target.damage(skill.power)
            messages += user.restore(skill.power)
            return messages

        obj.steps(calculate, apply)

        return obj

    def heal():
        obj = Skill(hint="Heal self")

        def calculate(skill, user, target):
            amount = 2 * user.current["int"]
            amount = min([amount, user.base["hp"]])
            skill.power = amount

        def apply(skill, user, target):
            return skill.source.restore(skill.power)

        obj.steps(calculate, apply)

        return obj


class Skills:
    def get(name):
        if type(name) is not str:
            name = name.name
        internal_name = internal(name)
        default_name = printable(internal_name)
        skill_func = getattr(SkillFuncs, internal_name)
        skill_obj = skill_func()
        if not skill_obj.name:
            assert "'" not in name  # Skills with quotes must always set name
            skill_obj.name = default_name
        return skill_obj

    names = [x for x in dir(SkillFuncs) if "__" not in x]
