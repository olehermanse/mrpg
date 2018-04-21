from mrpg.utils.utils import column_string, single_newline


class Battle():
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def stats(self):
        a = self.a.string_long(skills=False).split(sep="\n")
        b = self.b.string_long(skills=False).split(sep="\n")

        return column_string("| ", a, " | ", b, " |")

    def is_over(self):
        return self.a.is_dead() or self.b.is_dead()

    def pre_step(self, user, target):
        skill = user.use_skill
        skill.setup(user, target)
        return skill.calculate()

    def apply_step(self, user):
        return user.use_skill.apply()

    def one_player_turn(self, src, target):
        out = []
        out += self.pre_step(src, target)
        out += self.apply_step(src)
        out += src.limit_check()
        out += target.limit_check()
        single_newline(out)
        return out

    def effect_resolve(self):
        out = []
        # Check once here, because creatures may be "temporarily" dead
        a = self.a.is_alive()
        b = self.b.is_alive()
        if a:
            out += self.a.clean_effects()
        if b:
            out += self.b.clean_effects()
        if a:
            out += self.a.calculate_effects()
        if b:
            out += self.b.calculate_effects()
        if a:
            out += self.a.apply_effects()
        if b:
            out += self.b.apply_effects()
        if a:
            out += self.a.limit_check()
        if b:
            out += self.b.limit_check()
        if self.a.is_alive():
            out += self.a.tick_effects()
            out += self.a.clean_effects()
        if self.b.is_alive():
            out += self.b.tick_effects()
            out += self.b.clean_effects()

        single_newline(out)
        return out

    def sequential_turn(self, first, last):
        out = []
        out += self.one_player_turn(first, last)
        if last.is_alive():
            single_newline(out)
            out += self.one_player_turn(last, first)

        single_newline(out)

        return out + self.effect_resolve()

    def concurrent_turn(self, a, b):
        out = ["{} and {} acted at the same time!".format(a.name, b.name)]
        out += self.pre_step(a, b)
        out += self.pre_step(b, a)
        out += self.apply_step(a)
        single_newline(out)
        out += self.apply_step(b)
        single_newline(out)
        out += a.limit_check()
        out += b.limit_check()
        single_newline(out)
        return out + self.effect_resolve()

    def resolve_turn(self):
        a, b = self.a, self.b
        if a.current["dex"] == b.current["dex"]:
            return self.concurrent_turn(a, b)
        if a.current["dex"] < b.current["dex"]:
            a, b = b, a

        first, last = a, b
        return self.sequential_turn(first, last)
