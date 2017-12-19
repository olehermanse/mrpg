import json
import sys
import os
import argparse

sys.path.insert(0, "./")

from mrpg.platform.files import jsonify, json_load, save, load
from mrpg.core.creature import Creature
from mrpg.core.battle import Battle
from collections import OrderedDict
from mrpg.ui.terminal import menu, fancy_print, character_creator

def battle_loop(player):
    enemy = Creature("Ogre", 11)
    battle = Battle(player, enemy)
    while True:
        choice = menu("Battle Menu:", "turn", f="flee")
        if choice == "turn":
            results = battle.resolve_turn()
            fancy_print("\n".join(results))
            continue
        elif choice == "flee":
            fancy_print("{} fled like a big coward.".format(player.name))
            break

def game_loop(player):
    fancy_print("{} is ready to start an adventure".format(player))
    while True:
        choice = menu("Game Menu:", "stats", "battle", s="save", q="quit")
        if choice == "stats":
            print()
            print(player.string_long())
        elif choice == "battle":
            battle_loop(player)
        elif choice == "save":
            data = player.export_data()
            save(data, "data/player.json")
            fancy_print("Game has been saved")
        elif choice == "quit":
            fancy_print("Goodbye!")
            sys.exit(0)

def main_menu(args):
    player = Creature()
    while True:
        choice = menu("Main Menu:", "new", "load", q="quit")
        if choice == "new":
            player = character_creator()
        elif choice == "load":
            data = load("data/player.json")
            if not data:
                fancy_print("No saved game found")
                continue
            player.import_data(data)
        elif choice == "quit":
            fancy_print("Goodbye!")
            return
        game_loop(player)

def get_args():
    ap = argparse.ArgumentParser(description="MRPG",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--new",  help="Start new character", action="store_true")
    ap.add_argument("--test", help="Run test", action="store_true")
    args = ap.parse_args()
    return args

if __name__ == "__main__":
    args = get_args()
    main_menu(args)
