class Skill:
    def __init__(self, name, func):
        self.func = func
        self.name = name

    def prepare(self, src, target):
        self.resolver = self.func(src, target)
        return []

    def resolve(self):
        return self.resolver()

class Skills:
    def attack(user, target):
        damage = user.current["str"] - target.current["str"]
        if damage <= 0:
            damage = 1
        def resolve():
            return target.damage(damage)
        return resolve

    def heal(user, target):
        amount = user.current.int
        def resolve():
            return target.restore(amount)
        return resolve

    @classmethod
    def get(cls, name):
        return Skill(name, getattr(cls, name))
