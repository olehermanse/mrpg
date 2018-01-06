
class Battle():
    def __init__(self, a,b):
        self.a = a
        self.b = b

    def pre_step(self, src, target):
        return src.use_skill.prepare(src, target)

    def apply_step(self, src, target):
        return src.use_skill.resolve()

    def one_player_turn(self, src, target):
        s = []
        s += self.pre_step(src, target)
        s += self.apply_step(src, target)
        return s

    def resolve_turn(self):
        a,b = self.a, self.b

        s = []
        s += self.one_player_turn(a,b)
        s += self.one_player_turn(b,a)

        return s
