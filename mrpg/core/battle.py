class Battle():
    def __init__(self, a, b):
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
        s += src.limit_check()
        s += target.limit_check()
        return s

    def speed_tie(self, a, b):
        s = ["{} and {} acted at the same time!".format(a.name, b.name)]
        s += self.pre_step(a, b)
        s += self.pre_step(b, a)
        s += self.apply_step(a, b)
        s += self.apply_step(b, a)
        s += a.limit_check()
        s += b.limit_check()
        return s

    def resolve_turn(self):
        a, b = self.a, self.b
        if a.current["dex"] == b.current["dex"]:
            return self.speed_tie(a, b)
        if a.current["dex"] < b.current["dex"]:
            a, b = b, a

        first, last = a, b

        s = []
        s += self.one_player_turn(first, last)
        if last.is_alive():
            s += self.one_player_turn(last, first)

        return s
