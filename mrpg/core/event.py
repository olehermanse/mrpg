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
            effect=None,
            dead=None,
            reduction=None,
            func=None,
            mana=None,
            mana_cost=None,
            used=False,
            pause=False,
            limit=False):

        self.damage = damage
        self.skill = skill
        self.user = user
        self.source = source
        self.target = target
        self.message = message
        self.messages = messages
        self.restore = restore
        self.effect = effect
        self.dead = dead
        self.func = func
        self.mana = mana
        self.reduction = reduction
        self.pause = pause
        self.limit = limit

    def __str__(self):
        return "{} - {} - {} - {}".format(self.skill, self.user, self.source, self.message)

    def apply(self):
        outputs = []
        if self.pause:
            outputs.append("")
        if self.message is not None:
            outputs.append(self.message)
        elif self.messages is not None:
            outputs.extend(self.messages)
        elif self.skill and self.user:
            outputs.append(
                "{} used {}".format(self.user.name, self.skill.name))

        if self.reduction:
            current = self.target.current
            for stat in self.reduction:
                current[stat] -= self.reduction[stat]
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
        if self.effect:
            self.target.add_effect(self.effect)
            outputs.append(
                "{} gained {}".format(self.target.name, self.effect.name))
        if self.dead:
            self.target.kill()
            outputs.append("{} died.".format(self.target.name))

        if self.limit:
            self.target.limit_check()

        return outputs

    @staticmethod
    def pause():
        return Event(pause=True)

    @staticmethod
    def apply_all(all):
        outputs = []
        for outcome in all:
            output = outcome.apply()
            if not output:
                continue
            if type(output) is str:
                outputs.append(output)
            else:
                outputs += output
        return outputs

def add_pause(l):
    return
    if len(l) == 0 or l[-1] is None or l[-1].pause is False:
        l.append(Event.pause())