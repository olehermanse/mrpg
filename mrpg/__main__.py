import json
import sys
import os
import argparse

sys.path.insert(0, "./")

from mrpg.files import jsonify, json_load, save, load
from mrpg.core.creature import Creature
from collections import OrderedDict

def create(overwrite_new=False):
    player = Creature()
    data = load("data/player.json")
    if not data or overwrite_new:
        player.name  = input("Name:")
        player.level = int(input("Level:"))
        data = player.export_data()
        save(data, "data/player.json")
    else:
        player.import_data(data)
    return player

def get_args():
    ap = argparse.ArgumentParser(description="MRPG",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--new", help="Start new character", action="store_true")
    args = ap.parse_args()
    return args

if __name__ == "__main__":
    args = get_args()

    player = create(args.new)
    print("{} is ready to start an adventure".format(player))
