from mrpg.utils.utils import printable, internal
from mrpg.core.event import Event


class Effect:
    def __init__(
            self,
            duration=None,
            hint=None,
            proc=None,
            modifier=None,
            name=None,
            skip=False,
            source=None,
            target=None):
        self.duration = duration
        self.hint = hint
        self._proc = proc
        self._modifier = modifier
        self.name = name
        self.skip = skip
        self.source = source
        self.target = target

    def __str__(self):
        return self.name

    def tick(self):
        assert self.duration is not None
        self.duration -= 1

    def is_done(self):
        return (self.duration <= 0)

    def proc(self):
        if self._proc:
            res = self._proc(self, self.source, self.target)
            if not res:
                return []
            if type(res) is not list:
                return [res]
            return res
        return []

    def modify(self):
        if self._modifier:
            res = self._modifier(self, self.source, self.target)
            if not res:
                return []
            if type(res) is not list:
                return [res]
            return res
        return []


class EffectFuncs:
    def burn():
        def proc(effect, skill, target):
            damage = max(effect.damage, 1)
            return Event(target=target, damage=damage, source=effect)

        return Effect(hint="Hot", proc=proc)

    def bleed():
        def proc(effect, skill, target):
            damage = max(1, target.base["hp"] // 10)
            return Event(target=target, damage=damage, source=effect)

        return Effect(hint="Ow", duration=5, proc=proc)

    def shock():
        def modifier(effect, skill, target):
            # Calculate a reduction which will be applied later:
            reduction = target.base["dex"] // 3
            return Event(target=target, reduction={"dex": reduction})

        return Effect(hint="Zap", duration=5, modifier=modifier)


class Effects:
    def get(name, skill=None, target=None):
        if type(name) is not str:
            name = name.name
        internal_name = internal(name)
        default_name = printable(internal_name)
        effect_func = getattr(EffectFuncs, internal_name)
        effect_obj = effect_func()
        if skill:
            effect_obj.skill = skill
        if target:
            effect_obj.target = target
        if not effect_obj.name:
            assert "'" not in name  # Effects with quotes must always set name
            effect_obj.name = default_name
        return effect_obj

    names = [x for x in dir(EffectFuncs) if "__" not in x]
