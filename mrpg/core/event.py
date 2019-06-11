class Event():
    def __init__(
            self,
            damage=None,
            skill=None,
            user=None,
            target=None,
            source=None,
            message=None,
            messages=None,
            restore=None,
            kill=None,
            reduction=None,
            func=None,
            mana=None,
            mana_cost=None,
            limit=False,
            effect=None,
            tick=False,
            clean=False,
            reset=False,
            proc=False,
            modify=False,
            events=None):

        self.damage = damage
        self.skill = skill
        self.user = user
        self.source = source
        self.target = target
        self.message = message
        self.messages = messages
        self.restore = restore
        self.kill = kill
        self.func = func
        self.mana = mana
        self.limit = limit
        self.effect = effect
        self.tick = tick
        self.clean = clean
        self.reset = reset
        self.proc = proc
        self.modify = modify
        self.reduction = reduction
        self.events = []

        for event in events or []:
            assert type(event) is Event
            self.events.append(event)

    def __str__(self):
        if self.events:
            return f"{len(self.events)} combined events"
        return f"{self.skill} - {self.user} - {self.source} - {self.message}"

    def resolve(self):
        outputs = []
        if self.message is not None:
            outputs.append(self.message)
        elif self.messages is not None:
            outputs.extend(self.messages)
        elif self.skill and self.user:
            outputs.append(f"{self.user.name} used {self.skill.name}.")

        if self.func:
            ret = self.func(self.target)
            if type(ret) is list:
                outputs += ret
            if type(ret) is str:
                outputs.append(str)
        if self.mana is not None:
            self.target.current["mp"] += self.mana
        if self.restore:
            outputs += self.target.restore(self.restore)
        if self.damage:
            outputs += self.target.damage(self.damage, source=self.source)

        # Effect related events:

        if self.effect:
            self.target.add_effect(self.effect)
            outputs.append(f"{self.target.name} gained {self.effect.name}.")

        if self.tick:
            self.target.tick_effects()

        if self.clean:
            names = self.target.clean_effects()
            for name in names:
                outputs.append(f"{self.target.name}'s {name} faded.")

        if self.reset:
            self.target.reset_stats()

        if self.proc:
            events = self.target.proc_effects()
            for event in events:
                outputs.extend(event.resolve())

        if self.modify:
            events = self.target.modify_effects()
            for event in events:
                outputs.extend(event.resolve())

        if self.reduction:
            current = self.target.current
            for stat in self.reduction:
                current[stat] -= self.reduction[stat]

        # Combined events:

        if self.events:
            for event in self.events:
                outputs.extend(event.resolve())

        # Bounding hp and mana between 0 and max, and kill if hp is 0:

        if self.limit:
            should_kill = self.target.limit_check()
            if should_kill:
                self.kill = True

        if self.kill and self.target.is_alive():
            self.target.kill()
            outputs.append(f"{self.target.name} died.")

        # Return a list of strings to print, may be empty:

        return outputs
