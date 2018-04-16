from collections import OrderedDict

from mrpg.core.skill import Skill


class SkillFuncs:
    def attack(user, target, hint=False):
        if hint:
            return "Physical attack"
        usr, tar = user.current, target.current
        damage = 2 * usr["str"]
        damage -= tar["str"]
        damage = max([damage, 1])

        def resolve():
            return target.damage(damage)

        return resolve

    def fireball(user, target, hint=False):
        if hint:
            return "Hot magic"
        usr, tar = user.current, target.current
        damage = 2 * usr["int"]
        damage -= tar["int"]
        damage = max([damage, 1])

        def resolve():
            return target.damage(damage)

        return resolve

    def life_drain(user, target, hint=False):
        if hint:
            return "Damage and restore"
        usr, tar = user.current, target.current
        amount = 3 * usr["int"] // 2
        amount -= tar["int"]
        amount = max([amount, 2])
        amount = min([amount, user.base["hp"]])

        def resolve():
            return target.damage(amount) + user.restore(amount)

        return resolve

    def heal(user, target, hint=False):
        if hint:
            return "Heal self"
        amount = 2 * user.current["int"]
        amount = min([amount, user.base["hp"]])

        def resolve():
            return user.restore(amount)

        return resolve


class Skills:
    def get(name):
        if type(name) is not str:
            name = name.name
        name = name.lower()
        name = name.replace(" ", "_")
        skill_func = getattr(SkillFuncs, name)
        hint = skill_func(None, None, hint=True)
        return Skill(name, skill_func, hint)

    names = [x for x in dir(SkillFuncs) if "__" not in x]
