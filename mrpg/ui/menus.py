import sys

from mrpg.core.creature import Creature

from mrpg.platform.files import save, load
from mrpg.ui.terminal import menu, fancy_print, character_creator, clear
from mrpg.ui.battle import battle_loop

def game_menu(player):
    while True:
        clear()
        choice = menu("Game Menu:", "battle", "stats", s="save", q="quit")
        if choice == "stats":
            clear()
            print(player.string_long())
            input()
        elif choice == "battle":
            enemy = Creature("Ogre", 10)
            winner = battle_loop(player, enemy)
            if not player.is_alive():
                clear()
                fancy_print("Game over")
                return
        elif choice == "save":
            data = player.export_data()
            save(data, "data/player.json")
            fancy_print("Game has been saved")
        elif choice == "quit":
            fancy_print("Goodbye!", block=False)
            sys.exit(0)

def main_menu(args):
    player = Creature()
    while True:
        clear()
        choice = menu("Main Menu:", "new", "load", q="quit")
        if choice == "new":
            player = character_creator()
            fancy_print("Hello, {}.".format(player.name))
        elif choice == "load":
            data = load("data/player.json")
            if not data:
                fancy_print("No saved game found")
                continue
            player.import_data(data)
            fancy_print("Welcome back, {}.".format(player.name))
        elif choice == "quit":
            fancy_print("Goodbye!", block=False)
            return
        game_menu(player)
