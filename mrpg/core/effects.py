from mrpg.utils.utils import printable, internal
from mrpg.core.applier import Applier

class Effect(Applier):
    def __init__(
            self,
            duration=None,
            **kwargs):
        super().__init__(**kwargs)
        self.skip_calc = False
        self.duration = duration

    def tick(self):
        assert self.duration is not None
        self.duration -= 1

    def is_done(self):
        return (self.duration <= 0)


class EffectFuncs:
    def burn():
        obj = Effect(hint="Hot", duration=1)

        def calculate(effect, skill, target):
            effect.power = skill.power // 3

        def apply(effect, skill, target):
            return target.damage(effect.power, source=effect.name)

        obj.steps(calculate, apply)

        return obj


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
