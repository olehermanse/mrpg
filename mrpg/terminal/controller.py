from mrpg.core.game import Game, State
from mrpg.terminal.io import clear, fancy_print


class Controller():
    def __init__(self):
        self.game = Game()

    def print_output(self):
        while self.game.events:
            event = self.game.get_event()
            messages = event.resolve()
            messages = [s.strip() for s in messages if s.strip()]
            if not messages:
                continue
            for msg in messages[:-1]:
                fancy_print(msg, block=False)
            fancy_print(messages[-1], block=True)

    def run(self):
        while True:
            clear()
            self.print_output()
            if self.game.state is State.BATTLE:
                print(self.game.battle.stats())
                print()
            if self.game.state is State.GAME_MENU:
                print(self.game.player.string_long())
                print()
            if self.game.menu:
                print(self.game.menu.as_string())
            choice = input("> ")
            self.game.submit(choice)
            self.print_output()
