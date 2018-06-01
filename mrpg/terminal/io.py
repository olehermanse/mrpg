from time import sleep

from mrpg.core.creature import Creature
from mrpg.core.skills import Skills
from mrpg.utils.menu import Menu

import sys
import os


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    sys.stdout.flush()


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
    player.set_level(1)
    # player.set_level(level=int(input("Level: ")))
    # skill_names = skill_picker(8)
    skill_names = ['Attack', 'Heal']
    player.skills.learn(skill_names)
    player.skills.equip(skill_names)
    return player


def terminal_menu(menu_object):
    while True:
        print(menu_object.as_string())
        choice = menu_object.choice(input("> "))
        if choice is not None:
            return choice


def menu(*args, **kwargs):
    """Print a menu in terminal and get input until valid

    Example:
        choice = menu("Main menu:", "save", "load", q="quit")
        if choice == "quit":
            sys.exit(0)
    """
    return terminal_menu(Menu(*args, **kwargs))
