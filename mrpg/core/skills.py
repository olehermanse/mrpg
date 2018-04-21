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
            skill.power = 2 * user.current["str"]
            skill.damage = target.mitigation(skill.power, "physical")

        def apply(skill, user, target):
            return target.damage(skill.damage)

        return Skill(hint="Physical attack", calculate=calculate, apply=apply)

    def heal():
        def calculate(skill, user, target):
            skill.power = 2 * user.current["int"]
            skill.healing = min([skill.power, user.base["hp"]])

        def apply(skill, user, target):
            return skill.source.restore(skill.healing)

        return Skill(hint="Heal self", calculate=calculate, apply=apply)

    def fireball():
        def calculate(skill, user, target):
            skill.power = 2 * user.current["int"]
            skill.damage = target.mitigation(skill.power, "magic")

        def apply(skill, user, target):
            burn = Effects.get("burn", skill=skill, target=target)
            burn.message = "{} was burned".format(target.name)
            ret = target.damage(skill.damage)
            target.add_effect(burn)
            return ret

        return Skill(hint="Hot magic", calculate=calculate, apply=apply)

    def life_drain():
        def calculate(skill, user, target):
            usr = user.current
            skill.power = 3 * usr["int"] // 2
            amount = target.mitigation(skill.power, "magic")
            skill.damage = limit(amount, 2, user.base["hp"])

        def apply(skill, user, target):
            messages = []
            messages += target.damage(skill.damage)
            messages += user.restore(skill.damage)
            return messages

        return Skill(
            hint="Damage and restore", calculate=calculate, apply=apply)

    def blood_pact():
        def calculate(skill, user, target):
            skill.damage = skill.healing = user.base["hp"]

        def apply(skill, user, target):
            target = user
            bleed = Effects.get("Bleed")
            bleed.setup(skill, target)
            bleed.message = "{} started bleeding".format(target.name)
            target.add_effect(bleed)
            return skill.source.restore(skill.healing)

        return Skill(
            hint="Fully heal, but start bleeding",
            calculate=calculate,
            apply=apply)


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
