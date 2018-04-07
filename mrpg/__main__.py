#!/usr/bin/env python3
"""RPG in progress"""

import argparse


def get_args():
    ap = argparse.ArgumentParser(
        description="MRPG",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args = ap.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    main_menu()
