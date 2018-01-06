import sys

from mrpg.core.creature import Creature

from mrpg.platform.files import save, load
from mrpg.ui.terminal import menu, fancy_print, character_creator, clear
from mrpg.ui.gameplay import start_adventure, GameOver

def game_menu(player):
    while True:
        clear()
        choice = menu("Game Menu:", "adventure", "stats", s="save", q="quit")
        if choice == "stats":
            clear()
            print(player.string_long())
            input()
        elif choice == "adventure":
            start_adventure(player)
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
        try:
            game_menu(player)
        except GameOver:
            clear()
            fancy_print("Game over")
            continue
