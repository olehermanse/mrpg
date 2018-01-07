from mrpg.core.skill import Skill

class Skills:
    @classmethod
    def get(cls, name):
        skill_func = getattr(cls, name)
        hint = skill_func(None, None, hint=True)
        return Skill(name, skill_func, hint)

    def attack(user, target, hint=False):
        if hint:
            return "Physical attack"
        usr, tar = user.current, target.current
        damage = 3 * (usr["str"] + usr["dex"]) // 2
        damage -= tar["str"] + tar["dex"]
        damage = max([damage, 1])
        def resolve():
            return target.damage(damage)
        return resolve

    def fireball(user, target, hint=False):
        if hint:
            return "Hot magic"
        usr, tar = user.current, target.current
        damage = 2 * usr["int"] - tar["int"]
        damage = max([damage, 1])
        def resolve():
            return target.damage(damage)
        return resolve

    def life_drain(user, target, hint=False):
        if hint:
            return "Damage and restore"
        usr, tar = user.current, target.current
        amount = usr["int"] - tar["int"]
        amount = max([amount, 2])
        amount = min([amount, user.base["hp"]])
        def resolve():
            return target.damage(amount) + user.restore(amount)
        return resolve

    def heal(user, target, hint=False):
        if hint:
            return "Heal self"
        amount = user.current["int"]
        amount = min([amount, user.base["hp"]])
        def resolve():
            return user.restore(amount) # TODO: Add targetable heal?
        return resolve
