class Skill:
    def __init__(self, name, func, hint):
        self.func = func
        self.hint = hint
        name = name[0].upper() + name[1:]
        self.name = name.replace("_", " ")

    def prepare(self, src, target):
        self.resolver = self.func(src, target)
        return []

    def resolve(self):
        return self.resolver()
