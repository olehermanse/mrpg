from mrpg.utils.utils import printable, internal


class SkillUse:
    def __init__(self, name=None, hint=None):
        self.name = name
        self.hint = hint
        self.preparer = None
        self.resolver = None
        self.user = None
        self.target = None

    def func_pair(self, preparer, resolver):
        self.preparer, self.resolver = preparer, resolver

    def prepare(self, user, target):
        skill = self
        self.user = user
        self.target = target
        res = self.preparer(skill, user, target)
        if not res:
            return []
        return res

    def resolve(self):
        return self.resolver(self, self.user, self.target)


class SkillFuncs:
    def attack():
        obj = SkillUse(hint="Physical attack")

        def prepare(skill, user, target):
            usr, tar = user.current, target.current
            damage = 2 * usr["str"]
            damage -= tar["str"]
            damage = max([damage, 1])
            skill.power = damage

        def resolve(skill, user, target):
            return target.damage(skill.power)

        obj.func_pair(prepare, resolve)

        return obj

    def fireball():
        obj = SkillUse(hint="Hot magic")

        def prepare(skill, user, target):
            usr, tar = user.current, target.current
            damage = 2 * usr["int"]
            damage -= tar["int"]
            damage = max([damage, 1])
            skill.power = damage

        def resolve(skill, user, target):
            return target.damage(skill.power)

        obj.func_pair(prepare, resolve)

        return obj

    def life_drain():
        obj = SkillUse(hint="Damage and restore")

        def prepare(skill, user, target):
            usr, tar = user.current, target.current
            amount = 3 * usr["int"] // 2
            amount -= tar["int"]
            amount = max([amount, 2])
            amount = min([amount, user.base["hp"]])
            skill.power = amount

        def resolve(skill, user, target):
            return target.damage(skill.power) + user.restore(skill.power)

        obj.func_pair(prepare, resolve)

        return obj

    def heal():
        obj = SkillUse(hint="Heal self")

        def prepare(skill, user, target):
            amount = 2 * user.current["int"]
            amount = min([amount, user.base["hp"]])
            skill.power = amount

        def resolve(skill, user, target):
            return skill.user.restore(skill.power)

        obj.func_pair(prepare, resolve)

        return obj


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
