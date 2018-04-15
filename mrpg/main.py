#!/usr/bin/env python3
"""RPG in progress"""

import argparse


def get_args():
    ap = argparse.ArgumentParser(
        description="MRPG",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--terminal", help="Terminal only", action="store_true")
    args = ap.parse_args()
    return args


def main():
    args = get_args()
    if args.terminal:
        from mrpg.terminal.controller import Controller
        Controller().run()
    else:
        from mrpg.gui.controller import Controller
        Controller().run()


if __name__ == "__main__":
    main()
