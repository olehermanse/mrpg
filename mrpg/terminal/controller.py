from mrpg.core.game import Game, Output, State
from mrpg.terminal.io import clear, fancy_print


class Controller():
    def __init__(self):
        self.game = Game()

    def print_output(self):
        messages = self.game.get_output()
        if not messages:
            return
        for msg in messages:
            if type(msg) is Output.Fancy:
                fancy_print(msg.data, block=False)
            elif type(msg) is Output.Display:
                clear()
                print(msg.data)
            else:
                raise AssertionError
        fancy_print("")

    def run(self):
        while True:
            clear()
            self.print_output()
            if self.game.state is State.BATTLE_MENU:
                print(self.game.battle.stats())
                print()
            if self.game.menu:
                print(self.game.menu.as_string())
            choice = input("> ")
            self.game.submit(choice)
            self.print_output()