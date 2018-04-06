from time import sleep

from mrpg.core.creature import Creature
from mrpg.core.skills import Skills
from mrpg.utils import column_string

import sys


def clear():
    sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.flush()


def skill_picker(max_skills):
    remaining_skills = [x for x in Skills.names]
    picked_skills = []
    counter = 1
    while counter <= max_skills and remaining_skills:
        clear()
        if picked_skills:
            print("Your skills:")
            [print(picked) for picked in picked_skills]
            print()
        choice = menu(
            "Pick skill no.{}/{}".format(counter, max_skills),
            *remaining_skills)
        picked_skills.append(choice)
        remaining_skills.remove(choice)
        counter += 1
    return picked_skills


def character_creator():
    clear()
    player = Creature()
    player.name = input("Name: ")
    player.set_level(level=int(input("Level: ")))
    skill_names = skill_picker(8)
    player.set_skills(skill_names)
    return player


def menu(*args, **kwargs):
    headline = args[0]
    args = list(args[1:])
    args_len = len(args)
    lst = None
    hints = None
    hints_sep = None

    if "lst" in kwargs:
        lst = kwargs["lst"]
        del kwargs["lst"]
        for item in lst:
            args.append(item)
    if "hints" in kwargs:
        hints = kwargs["hints"]
        hints_sep = len(hints) * [" - "]
        del kwargs["hints"]
        if args_len > 0:
            hints = [""] * args_len + hints
            hints_sep = [""] * args_len + hints_sep

    extended_args = []
    indices = list(range(1, len(args) + 1))
    for key, value in kwargs.items():
        indices.append(key)
        extended_args.append(value)
    for index, arg in enumerate(args):
        kwargs[str(index + 1)] = arg
    args += extended_args
    while hints and len(hints) < len(args):
        hints.append("")
        hints_sep.append("")
    while True:
        print(headline)
        if hints:
            print(column_string(indices, ": ", args, hints_sep, hints))
        else:
            print(column_string(indices, ": ", args))
        choice = input(">").strip()
        if choice in args:
            return choice
        try:
            return kwargs[choice]
        except KeyError:
            pass


def fancy_print(msg, block=True):
    if isinstance(msg, list):
        msg = "\n".join(msg)
    delay = 0.03
    if len(msg) > 16:
        delay = 0.01
    for c in msg:
        print(c, end="", flush=True)
        sleep(delay)
    sleep(0.1)
    if block:
        input()
    else:
        print()
