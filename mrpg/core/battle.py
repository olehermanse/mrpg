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


class Battle:
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
        assert user.use_skill
        skill = user.use_skill
        user.use_skill = None
        skill.setup(user, target)
        s = skill.use()
        return s

    def update_stats(self):
        events = []
        events.append(Event(target=self.a, reset=True))
        events.append(Event(target=self.a, modify=True))
        events.append(Event(target=self.b, reset=True))
        events.append(Event(target=self.b, modify=True))
        return Event(events=events)

    def update_effects(self):
        events = []
        events.append(Event(target=self.a, clean=True))
        events.append(Event(target=self.b, clean=True))
        events.append(self.update_stats())
        return Event(events=events)

    def one_player_turn(self, src, target):
        events = []
        events += self.skill_use(src, target)
        events.append(self.update_stats())
        events.append(self.limit_checks())
        yield Event(events=events)
        yield self.update_effects()

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
        for event in self.one_player_turn(first, last):
            yield event

        # At this point, yielded events must be resolved so check works:
        if last.is_alive():
            for event in self.one_player_turn(last, first):
                yield event

    def concurrent_turn(self, a, b):
        events = []
        msg = Event(message=f"{a} and {b} acted at the same time!")
        events.append(msg)
        events += self.skill_use(a, b)
        events += self.skill_use(b, a)
        events.append(self.update_stats())
        events.append(self.limit_checks())
        yield Event(events=events)

    def skill_step(self):
        a, b = self.a, self.b
        a_speed, b_speed = a.current["dex"], b.current["dex"]
        a_priority, b_priority = a.use_skill.priority, b.use_skill.priority
        if a_priority == b_priority and a_speed == b_speed:
            for event in self.concurrent_turn(a, b):
                assert type(event) is Event
                yield event
            return
        if a_priority < b_priority or (a_speed < b_speed and a_priority == b_priority):
            a, b = b, a
        first, last = a, b
        for event in self.sequential_turn(first, last):
            assert type(event) is Event
            yield event

    def effect_step_creature(self, creature):
        events = []
        events.append(Event(target=creature, clean=True))  # Remove expired
        events.append(Event(target=creature, reset=True))  # Reset stats
        events.append(Event(target=creature, modify=True))  # Apply modifiers
        events.append(Event(target=creature, proc=True))  # Proc effect
        events.append(Event(target=creature, limit=True))  # Maybe dead
        return Event(events=events)  # Everything happens "at once"

    def effect_step(self):
        events = []
        a, b = self.a, self.b
        a_alive, b_alive = a.is_alive(), b.is_alive()
        if a_alive:
            events.append(self.effect_step_creature(a))
        if b_alive:
            events.append(self.effect_step_creature(b))

        yield Event(events=events)

    def end_step_creature(self, creature):
        events = []
        events.append(Event(target=creature, tick=True))  # Decrease duration
        events.append(Event(target=creature, clean=True))  # Remove expired
        events.append(Event(target=creature, reset=True))  # Reset stats
        events.append(Event(target=creature, modify=True))  # Apply modifiers
        return Event(events=events)  # Everything happens "at once"

    def end_step(self):
        events = []
        a, b = self.a, self.b
        a_alive, b_alive = a.is_alive(), b.is_alive()
        a_hp, b_hp = a.current["hp"], b.current["hp"]

        if a_alive:
            events.append(self.end_step_creature(a))
        if b_alive:
            events.append(self.end_step_creature(b))

        yield Event(events=events)  # Everything happens "at once"

        # Check that we didn't modify anything:
        assert a_alive == a.is_alive()
        assert b_alive == b.is_alive()
        assert a_hp == a.current["hp"]
        assert b_hp == b.current["hp"]
