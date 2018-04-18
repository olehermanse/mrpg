from mrpg.utils.utils import printable, internal


class Effect:
    def __init__(self, name=None, hint=None, duration=None):
        self.name = name
        self.hint = hint
        self.duration = duration
        self.preparer = None
        self.applier = None
        self.skill = None
        self.target = None
        self.skip_calc = False
        self.message = None

    def func_pair(self, calc, apply):
        self.calculator = calc
        self.applier = apply

    def setup(self, skill, target):
        effect = self
        effect.skill = skill
        effect.target = target

    def calculate(self):
        if self.calculator and not self.skip_calc:
            return self.calculator(self, self.skill, self.target)
        return []

    def apply(self):
        assert self.applier
        return self.applier(self, self.target)

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

        def apply(effect, target):
            return target.damage(effect.power, source=effect.name)

        obj.func_pair(calculate, apply)

        return obj


class Effects:
    def get(name, skill=None):
        if type(name) is not str:
            name = name.name
        internal_name = internal(name)
        default_name = printable(internal_name)
        effect_func = getattr(EffectFuncs, internal_name)
        effect_obj = effect_func()
        if skill:
            effect_obj.skill = skill
        if not effect_obj.name:
            assert "'" not in name  # Effects with quotes must always set name
            effect_obj.name = default_name
        return effect_obj

    names = [x for x in dir(EffectFuncs) if "__" not in x]
