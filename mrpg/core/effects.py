from mrpg.utils.utils import printable, internal


class Effect:
    def __init__(self, name=None, hint=None):
        self.name = name
        self.hint = hint
        self.preparer = None
        self.applier = None
        self.skill = None
        self.target = None

    def func_pair(self, preparer, applier):
        self.preparer, self.applier = preparer, applier

    def prepare(self, skill, target):
        effect = self
        self.skill = skill
        self.target = target
        res = self.preparer(effect, skill, target)
        if not res:
            return []
        return res

    def apply(self):
        effect = self
        target = self.target
        return self.applier(effect, target)


class EffectFuncs:
    def burn():
        obj = Effect(hint="Hot", duration=3)

        def prepare(effect, skill, target):
            effect.power = skill.power // 3

        def apply(effect, target):
            return target.damage(effect.power)

        obj.func_pair(prepare, apply)

        return obj


class Effects:
    def get(name):
        if type(name) is not str:
            name = name.name
        internal_name = internal(name)
        default_name = printable(internal_name)
        effect_func = getattr(EffectFuncs, internal_name)
        effect_obj = effect_func()
        if not effect_obj.name:
            assert "'" not in name  # Effects with quotes must always set name
            effect_obj.name = default_name
        return effect_obj

    names = [x for x in dir(EffectFuncs) if "__" not in x]
