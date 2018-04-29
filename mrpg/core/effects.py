from mrpg.utils.utils import printable, internal
from mrpg.core.applier import Applier


class Effect(Applier):
    def __init__(self, duration=None, **kwargs):
        super().__init__(**kwargs)
        self.duration = duration

    def tick(self):
        assert self.duration is not None
        self.duration -= 1

    def is_done(self):
        return (self.duration <= 0)


class EffectFuncs:
    def burn():
        def calculate(effect, skill, target):
            effect.damage = max(1, skill.damage // 4)

        def apply(effect, skill, target):
            return target.damage(effect.damage, source=effect.name)

        return Effect(
            hint="Hot", duration=3, calculate=calculate, apply=apply)

    def bleed():
        def calculate(effect, skill, target):
            effect.damage = skill.damage // 5

        def apply(effect, skill, target):
            return target.damage(effect.damage, source=effect.name)

        return Effect(hint="Ow", duration=5, calculate=calculate, apply=apply)


class Effects:
    def get(name, skill=None, target=None):
        if type(name) is not str:
            name = name.name
        internal_name = internal(name)
        default_name = printable(internal_name)
        effect_func = getattr(EffectFuncs, internal_name)
        effect_obj = effect_func()
        effect_obj.setup(skill, target)
        if not effect_obj.name:
            assert "'" not in name  # Effects with quotes must always set name
            effect_obj.name = default_name
        return effect_obj

    names = [x for x in dir(EffectFuncs) if "__" not in x]
