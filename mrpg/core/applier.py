class Applier:
    def __init__(
            self,
            *,
            name=None,
            hint=None,
            apply=None,
            calculate=None,
            source=None,
            target=None,
            message=None):
        self.name = name
        self.hint = hint
        self._apply = apply
        self._calculate = calculate
        self.source = source
        self.target = target
        self.message = message
        self.skip_calc = False
        self.skip_apply = False

    def steps(self, calculate, apply):
        self._calculate, self._apply = calculate, apply

    def setup(self, source, target):
        self.source = source
        self.target = target

    def calculate(self):
        if self.skip_calc:
            return []
        res = []
        if self._calculate:
            res = self._calculate(self, self.source, self.target)
        if not res:
            return []
        return res

    def apply(self):
        if self.skip_apply:
            return []
        res = []
        if self._apply:
            res = self._apply(self, self.source, self.target)
        if not res:
            return []
        return res
