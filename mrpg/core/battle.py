
class Battle():
    def __init__(self, a,b):
        self.a = a
        self.b = b
        self.a_choice = None
        self.b_choice = None

    def resolve_turn(self):
        return [
            "{} did nothing.".format(self.a.name),
            "{} did nothing.".format(self.b.name)
        ]
