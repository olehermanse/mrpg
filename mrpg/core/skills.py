from mrpg.utils.utils import printable, internal, limit
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
        def calculate(skill, user, target):
            power = 2 * user.current["str"]
            damage = target.mitigation(power, "physical")
            skill.power = damage

        def apply(skill, user, target):
            return target.damage(skill.power)

        return Skill(hint="Physical attack", calculate=calculate, apply=apply)

    def fireball():
        def calculate(skill, user, target):
            power = 2 * user.current["int"]
            damage = target.mitigation(power, "magic")
            skill.power = damage

        def apply(skill, user, target):
            burn = Effects.get("burn", skill=skill, target=target)
            burn.message = "{} was burned".format(target.name)
            ret = target.damage(skill.power)
            ret += target.add_effect(burn, source=skill.name)
            return ret

        return Skill(hint="Hot magic", calculate=calculate, apply=apply)

    def life_drain():
        def calculate(skill, user, target):
            usr = user.current
            amount = 3 * usr["int"] // 2
            amount = target.mitigation(amount, "magic")
            amount = limit(amount, 2, user.base["hp"])
            skill.power = amount

        def apply(skill, user, target):
            messages = []
            messages += target.damage(skill.power)
            messages += user.restore(skill.power)
            return messages

        return Skill(
            hint="Damage and restore", calculate=calculate, apply=apply)

    def heal():
        def calculate(skill, user, target):
            amount = 2 * user.current["int"]
            amount = min([amount, user.base["hp"]])
            skill.power = amount

        def apply(skill, user, target):
            return skill.source.restore(skill.power)

        return Skill(hint="Heal self", calculate=calculate, apply=apply)


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
