#!/usr/bin/env python3
"""RPG in progress"""

import argparse

from mrpg.ui.menus import main_menu


def get_args():
    ap = argparse.ArgumentParser(
        description="MRPG",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--new", help="Start new character", action="store_true")
    ap.add_argument("--test", help="Run test", action="store_true")
    args = ap.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    main_menu(args)
