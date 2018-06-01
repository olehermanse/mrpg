from mrpg.utils.utils import column_string, single_newline
from mrpg.core.event import Event, add_pause


class Battle():
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def stats(self):
        a = self.a.string_long(skills=False).split(sep="\n")
        b = self.b.string_long(skills=False).split(sep="\n")

        return column_string("| ", a, " | ", b, " |")

    def end(self):
        self.a.battle_end()
        self.b.battle_end()

    def is_over(self):
        return self.a.is_dead() or self.b.is_dead()

    def skill_use(self, user, target):
        skill = user.use_skill
        skill.setup(user, target)
        s = skill.use()
        return s

    def apply(self, outcomes):
        return Event.apply_all(outcomes)

    def skill_use_apply(self, user, target):
        return self.apply(self.skill_use(user, target))

    def one_player_turn(self, src, target):
        outcomes = []
        outcomes += self.skill_use(src, target)
        outcomes += self.limit_checks()
        outcomes += self.clean_effects()
        return outcomes

    def clean_effects(self):
        out = []
        if self.a.is_alive():
            out += self.a.clean_effects()
        if self.b.is_alive():
            out += self.b.clean_effects()
        return out

    def limit_checks(self):
        out = []
        out += self.a.limit_check()
        out += self.b.limit_check()
        return out

    def sequential_turn(self, first, last):
        outcomes = []
        yield self.one_player_turn(first, last)
        if last.is_alive():
            yield self.one_player_turn(last, first)

        return outcomes

    def concurrent_turn(self, a, b):
        outcomes = []
        msg = Event(
            message="{} and {} acted at the same time!".format(a, b))
        outcomes.append(msg)
        outcomes += self.skill_use(a, b)
        outcomes += self.skill_use(b, a)
        outcomes.append(Event(limit=True, target=a))
        outcomes.append(Event(limit=True, target=b))
        add_pause(outcomes)
        return outcomes

    def skill_step(self):
        self.limit_checks()
        a, b = self.a, self.b
        if a.current["dex"] == b.current["dex"]:
            yield self.concurrent_turn(a, b)
            return
        if a.current["dex"] < b.current["dex"]:
            a, b = b, a
        first, last = a, b
        for outcomes in self.sequential_turn(first, last):
            yield outcomes

    def effect_step(self):
        out = []
        self.a.reset_stats()
        self.b.reset_stats()

        out += self.limit_checks()
        out += self.clean_effects()

        a, b = self.a.is_alive(), self.b.is_alive()
        if a:
            out += self.a.modify_effects()
            out += self.a.proc_effects()
        if b:
            out += self.b.modify_effects()
            out += self.b.proc_effects()

        add_pause(out)
        return out

    def end_step(self):
        out = []
        out += self.limit_checks()
        if self.a.is_alive():
            out += self.a.tick_effects()
            out += self.a.clean_effects()
            self.a.reset_stats()
            out += self.a.modify_effects()
        if self.b.is_alive():
            out += self.b.tick_effects()
            out += self.b.clean_effects()
            self.b.reset_stats()
            out += self.b.modify_effects()

        self.a.reset_stats()
        self.b.reset_stats()

        return out

    def turn(self):
        for outcomes in self.skill_step():
            yield outcomes
        yield self.effect_step()
        yield self.end_step()
