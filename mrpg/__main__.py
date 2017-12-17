import json
import sys
import os
import argparse

sys.path.insert(0, "./")

from mrpg.platform.files import jsonify, json_load, save, load
from mrpg.core.creature import Creature
from collections import OrderedDict
from mrpg.ui.creator import create
from mrpg.ui.term import menu

def game_loop(player):
    while True:
        print()
        choice = menu("Main Menu:", "stats", q="quit")
        if choice == "stats":
            print()
            print(player.string_long())
        elif choice == "quit":
            print("Goodbye!")
            sys.exit(0)

def get_args():
    ap = argparse.ArgumentParser(description="MRPG",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--new",  help="Start new character", action="store_true")
    ap.add_argument("--test", help="Run test", action="store_true")
    args = ap.parse_args()
    return args

if __name__ == "__main__":
    args = get_args()

    player = create(args.new, args.test)
    print("{} is ready to start an adventure".format(player))
    game_loop(player)
