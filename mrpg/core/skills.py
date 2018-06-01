from mrpg.utils.utils import printable, internal, limit
from mrpg.core.effects import Effects
from mrpg.core.event import Event


class Skill:
    def __init__(
            self,
            hint=None,
            use=None,
            name=None,
            skip=False,
            user=None,
            mana_cost=None,
            target=None):
        self.skip = skip
        self.hint = hint
        self._use = use
        self.user = user
        self.name = name
        self._mana_cost = mana_cost

    def __str__(self):
        return self.name

    def setup(self, user, target):
        self.user = user
        self.target = target

    @property
    def mana_cost(self):
        if not self._mana_cost:
            return None
        return self._mana_cost(self.user)

    def use(self):
        if self.skip:
            return []
        if not self._use:
            return []
        if self.mana_cost and self.mana_cost > self.user.current["mp"]:
            return [Event(message="Not enough mana")]
        outcomes = self._use(self, self.user, self.target)
        assert outcomes
        if type(outcomes) is not list:
            outcomes = [outcomes]
        assert type(outcomes[0]) is Event
        if self.mana_cost:
            mana = Event(mana=-self.mana_cost, target=self.user)
            outcomes = outcomes[0:1] + [mana] + outcomes[1:]
        outcomes[0].skill = self
        outcomes[0].user = self.user
        return outcomes


class SkillFuncs:
    def attack():
        def use(skill, user, target):
            power = 2 * user.current["str"]
            damage = target.mitigation(power, "physical")
            return Event(target=target, damage=damage)

        return Skill(hint="Physical attack", use=use)

    def heal():
        def use(skill, user, target):
            power = 2 * user.current["int"]
            healing = min(power, user.base["hp"])
            return Event(target=user, restore=healing)

        def mana_cost(user):
            return user.level + 2

        return Skill(hint="Heal self", use=use, mana_cost=mana_cost)

    def fireball():
        def use(skill, user, target):
            power = 2 * user.current["int"]
            damage = target.mitigation(power, "magic")

            burn = Effects.get("burn", skill=skill, target=target)
            burn.message = "{} was burned".format(target.name)
            burn.damage = damage // 5
            burn.duration = 5
            return Event(target=target, damage=damage, effect=burn)

        def mana_cost(user):
            return user.level + 2

        return Skill(hint="Hot magic", use=use, mana_cost=mana_cost)

    def life_drain():
        def use(skill, user, target):
            power = 3 * user.current["int"] // 2
            amount = target.mitigation(power, "magic")
            amount = limit(amount, 2, user.base["hp"])

            return [
                Event(damage=amount, target=target),
                Event(restore=amount, target=user)
            ]

        def mana_cost(user):
            return user.level + 2

        return Skill(hint="Damage and restore", use=use, mana_cost=mana_cost)

    def blood_pact():
        def use(skill, user, target):
            if user.has_effect("Bleed"):
                msg = None  # "{} bled out.".format(user.name)
                return Event(target=user, dead=True, message=msg)

            healing = user.base["hp"]
            bleed = Effects.get("Bleed", skill=skill, target=user)
            return Event(target=user, effect=bleed, restore=healing)

        return Skill(hint="Fully heal, but start bleeding", use=use)

    def lightning():
        def use(skill, user, target):
            power = 2 * user.current["int"]
            damage = target.mitigation(power, "magic")
            shock = Effects.get("Shock", skill=skill, target=target)
            return Event(target=target, effect=shock, damage=damage)

        def mana_cost(user):
            return user.level + 2

        return Skill(hint="Hurts and shocks", use=use, mana_cost=mana_cost)

    def true_strike():
        def use(skill, user, target):
            damage = user.current["dex"]
            return Event(target=target, damage=damage)

        return Skill(hint="Ignores damage mitigation", use=use)

    def slash():
        def use(skill, user, target):
            power = user.current["str"]
            damage = target.mitigation(power, "physical")

            bleed = Effects.get("Bleed", skill=skill, target=target)
            # bleed.message = "{} started bleeding".format(target.name)
            return Event(target=target, damage=damage, effect=bleed)

        return Skill(hint="Causes bleed", use=use)


class Skills:
    def get(name):
        if type(name) is not str:
            name = name.name
        internal_name = internal(name)
        default_name = printable(internal_name)
        skill_func = getattr(SkillFuncs, internal_name)
        skill_obj = skill_func()
        if not skill_obj.name:
            assert "'" not in name  # Skills with quotes must always set name
            skill_obj.name = default_name
        return skill_obj

    names = [x for x in dir(SkillFuncs) if "__" not in x]
