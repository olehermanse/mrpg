import json
import sys
import os
import argparse

sys.path.insert(0, "./")

from mrpg.platform.files import jsonify, json_load, save, load
from mrpg.core.creature import Creature
from mrpg.core.battle import Battle
from collections import OrderedDict
from mrpg.ui.terminal import menu, fancy_print, character_creator, clear
from mrpg.core.funcs import column_lines, column_string

def battle_loop(player):
    enemy = Creature("Ogre", 10)
    battle = Battle(player, enemy)
    while True:
        a = player.string_long().split(sep="\n")
        b = enemy.string_long().split(sep="\n")

        clear()
        print(column_string("| ", a, " | ", b, " |"))
        print()
        skill_names = player.get_skill_names()
        choice = menu("Battle Menu:", *skill_names, f="flee")

        if choice == "flee":
            fancy_print("{} fled like a big coward.".format(player.name))
            break
        if choice not in skill_names:
            assert False

        player.use_skill = player.get_skill(choice)
        enemy.use_skill = enemy.skills[0]

        results = battle.resolve_turn()
        fancy_print("\n".join(results))
        continue

def game_loop(player):
    while True:
        clear()
        choice = menu("Game Menu:", "battle", "stats", s="save", q="quit")
        if choice == "stats":
            clear()
            print(player.string_long())
            input()
        elif choice == "battle":
            battle_loop(player)
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
