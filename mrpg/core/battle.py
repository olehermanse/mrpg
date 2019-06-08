from mrpg.utils.utils import column_string, single_newline
from mrpg.core.event import Event


class Turn:
    def __init__(self, battle):
        self.battle = battle
        self.events = self.generator()

    def progress(self):
        assert self.events
        assert not self.is_over
        ret = next(self.events)

    def generator(self):
        for event in self.battle.skill_step():
            assert type(event) is Event
            yield event
        for event in self.battle.effect_step():
            assert type(event) is Event
            yield event
        for event in self.battle.end_step():
            assert type(event) is Event
            yield event


class Battle():
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.turn = None

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

    def one_player_turn(self, src, target):
        events = []
        events += self.skill_use(src, target)
        events.append(self.limit_checks())
        events.append(self.clean_effects())
        return events

    def clean_effects(self):
        events = []
        a, b = self.a, self.b
        if a.is_alive():
            events.append(Event(clean=True, target=a))
        if b.is_alive():
            events.append(Event(clean=True, target=b))
        return Event(events=events)

    def limit_checks(self):
        events = []
        events.append(Event(limit=True, target=self.a))
        events.append(Event(limit=True, target=self.b))
        return Event(events=events)

    def sequential_turn(self, first, last):
        events = list(self.one_player_turn(first, last))
        yield Event(events=events)

        # At this point, yielded events must be applied so check works:
        if last.is_alive():
            events = list(self.one_player_turn(last, first))
            yield Event(events=events)

    def concurrent_turn(self, a, b):
        events = []
        msg = Event(message="{} and {} acted at the same time!".format(a, b))
        events.append(msg)
        events += self.skill_use(a, b)
        events += self.skill_use(b, a)
        events.append(self.limit_checks())
        yield Event(events=events)

    def skill_step(self):
        a, b = self.a, self.b
        if a.current["dex"] == b.current["dex"]:
            for event in self.concurrent_turn(a, b):
                assert type(event) is Event
                yield event
            return
        if a.current["dex"] < b.current["dex"]:
            a, b = b, a
        first, last = a, b
        for event in self.sequential_turn(first, last):
            assert type(event) is Event
            yield event

    def effect_step(self):
        events = []
        self.a.reset_stats()
        self.b.reset_stats()

        events.append(self.clean_effects())

        a, b = self.a.is_alive(), self.b.is_alive()
        if a:
            events += self.a.modify_effects()
            events += self.a.proc_effects()
            events.append(self.limit_checks())
        if b:
            events += self.b.modify_effects()
            events += self.b.proc_effects()
            events.append(self.limit_checks())

        return events

    def end_step_creature(self, creature):
        events = []
        events.append(Event(target=creature, tick=True))  # Decrease duration
        events.append(Event(target=creature, clean=True))  # Remove expired
        events.append(Event(target=creature, reset=True))  # Reset stats
        events.append(Event(target=creature, modify=True))  # Apply modifiers
        return Event(events=events)  # Everything happens "at once"

    def end_step(self):
        a, b = self.a, self.b
        a_alive, b_alive = a.is_alive(), b.is_alive()
        a_hp, b_hp = a.current["hp"], b.current["hp"]

        if a_alive:
            yield self.end_step_creature(a)
        if b_alive:
            yield self.end_step_creature(b)

        # Check that we didn't modify anything:
        assert a_alive == a.is_alive()
        assert b_alive == b.is_alive()
        assert a_hp == a.current["hp"]
        assert b_hp == b.current["hp"]
