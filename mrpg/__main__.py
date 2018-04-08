#!/usr/bin/env python3
"""RPG in progress"""

import argparse


def get_args():
    ap = argparse.ArgumentParser(
        description="MRPG",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--gui", help="Graphics :)", action="store_true")
    args = ap.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    if args.gui:
        from mrpg.gui.controller import Controller
        Controller().run()
    else:
        from mrpg.terminal.controller import Controller
        Controller().run()
