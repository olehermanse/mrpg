from time import sleep

from mrpg.platform.files import save, load
from mrpg.core.creature import Creature

def character_creator():
    player = Creature()
    player.name = input("Name:")
    player.set_level(level = int(input("Level:")))
    data = player.export_data()
    return player

def menu(*args, **kwargs):
    headline = args[0]
    args = list(args[1:])
    extended_args = []
    indices = list(range(1,len(args)+1))
    for key, value in kwargs.items():
        indices.append(key)
        extended_args.append(value)
    for index, arg in enumerate(args):
        kwargs[str(index+1)] = arg
    args += extended_args
    while True:
        print()
        print(headline)
        for ind, opt in zip(indices, args):
            print("{}: {}".format(ind, opt))
        choice = input(">").strip()
        if choice in args:
            return choice
        try:
            return kwargs[choice]
        except:
            pass

def fancy_print(msg, block=True):
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
