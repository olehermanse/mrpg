import sys

from enum import Enum, unique, auto

from mrpg.utils.menu import Menu
from mrpg.utils.utils import flatten_strings, single_newline
from mrpg.system.files import save_data, load_data
from mrpg.core.creature import Creature
from mrpg.core.adventure import Adventure
from mrpg.core.battle import Battle
from mrpg.core.event import Event


def new_player():
    return Creature(
        "Alice",
        skill_names=[
            "attack", "heal", "fireball", "life_drain", "blood_pact",
            "lightning", "true_strike", "slash"
        ])

@unique
class State(Enum):
    MAIN_MENU = auto()
    GAME_MENU = auto()
    BATTLE = auto()
    NONE = auto()


class Game():
    def __init__(self):
        self.state = State.NONE
        self.menu = None
        self.player = None
        self.adventure = None
        self.output = []

        self.set_state(State.MAIN_MENU)

    def set_state(self, state):
        self.state = state
        if state == State.MAIN_MENU:
            self.adventure = None
            self.battle = None
            self.player = None
            self.menu = Menu("Main Menu:", "new", "load", q="quit")
        elif state == State.GAME_MENU:
            self.adventure = None
            self.battle = None
            self.menu = Menu(
                "Game Menu:", "adventure", s="save", q="quit")
        elif state == State.BATTLE:
            self.set_battle_menu()

    def set_battle_menu(self):
        player = self.player
        skill_names = player.skills.equipped.names()
        skill_hints = player.skills.equipped.hints()
        self.menu = Menu(
            "Battle Menu:", lst=skill_names, hints=skill_hints, f="flee")

    def main_menu_choice(self, choice):
        if choice == "new":
            self.player = new_player()
            self.put_output("Hello, {}.".format(self.player.name))
            self.set_state(State.GAME_MENU)
        elif choice == "load":
            data = load_data("data/player.json")
            if not data:
                self.put_output("No saved game found")
                return
            self.player = Creature()
            self.player.import_data(data)
            self.put_output("Welcome back, {}.".format(self.player.name))
            self.set_state(State.GAME_MENU)
        elif choice == "quit":
            sys.exit(0)  # TODO

    def game_menu_choice(self, choice):
        if choice == "adventure":
            self.adventure = Adventure(self.player)
            self.progress_adventure()
        elif choice == "save":
            data = self.player.export_data()
            save_data(data, "data/player.json")
            self.put_output("Save success!")
        elif choice == "quit":
            self.set_state(State.MAIN_MENU)

    def battle_menu_choice(self, choice):
        if choice == "flee":
            self.put_output(self.player.flee())
            self.end_battle()
            return
        self.battle.a.pick_skill(choice)
        self.battle.b.ai()
        self.progress_battle()

    def progress_battle(self):
        if self.battle.is_over():
            self.end_battle()
        out = []
        for outcomes in self.battle.turn():
            out += Event.apply_all(outcomes)
            out.append("")
        self.put_output(out)
        if self.battle.is_over():
            self.end_battle()

    def end_battle(self):
        player, enemy = self.battle.a, self.battle.b
        self.battle.end()
        self.battle = None
        if player.is_dead():
            self.put_output("Game over!")
            self.set_state(State.MAIN_MENU)
            return

        if enemy.is_dead():
            out = []
            out.append("Victory, you defeated {}.".format(enemy.name))
            out += player.gain_exp(enemy.exp_reward())
            single_newline(out)
            self.put_output(out)

        if self.adventure:
            self.progress_adventure()
        else:
            self.set_state(State.GAME_MENU)

    def new_battle(self):
        enemy = self.adventure.next_monster()
        self.put_output("A wild {} appeared".format(enemy.name))
        self.battle = Battle(self.player, enemy)
        self.set_state(State.BATTLE)
        pass

    def progress_adventure(self):
        if self.adventure.is_over():
            self.put_output(self.adventure.end())
            self.adventure = None
            self.battle = None
            self.player.full_heal()
            self.set_state(State.GAME_MENU)
        else:
            self.new_battle()

    def submit(self, choice):
        result = self.menu.choice(choice)
        if not result:
            return None
        state = self.state
        if state is State.MAIN_MENU:
            self.main_menu_choice(result)
        elif state is State.GAME_MENU:
            self.game_menu_choice(result)
        elif state is State.BATTLE:
            self.battle_menu_choice(result)

    def put_output(self, msg):
        strings = flatten_strings(msg)
        for s in strings:
            self.output.append(s)

    def get_output(self):
        output = self.output
        self.output = []
        return output
