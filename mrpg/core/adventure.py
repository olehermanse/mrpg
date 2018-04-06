from mrpg.core.creature import Creature
from mrpg.utils import limit
import random


def get_monster(player):
    level = player.level - random.randint(0, 5)
    level = limit(level, 1, 100)
    return Creature("Ogre", level, skill_names=["attack"])


def fail_message():
    msgs = ["The adventure was an embarassing failure.", "Failed adventure!"]
    return random.choice(msgs)
