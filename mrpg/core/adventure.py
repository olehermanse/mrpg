import random

from mrpg.core.creature import Creature
from mrpg.utils.utils import limit, single_newline


class Adventure:
    def __init__(self, player):
        self.player = player
        self.player.fleeing = False
        self.level = player.level
        self.monsters_left = 3

    def next_monster(self):
        self.monsters_left -= 1
        level = self.player.level - random.randint(0, 3)
        level = limit(level, 1, 100)
        skills = {
            "Ogre": ["attack"],
            "Cultist": ["attack", "life_drain", "blood_pact"],
            "Wizard": ["attack", "fireball", "heal", "lightning"],
            "Slime": ["attack", "heal", "slash", "true_strike"],
        }
        name = random.choice(list(skills))
        skills = skills[name]
        return Creature(name, level, skill_names=skills)

    def is_over(self):
        if self.player.fleeing:
            return True
        return self.monsters_left <= 0

    def end(self):
        player = self.player
        if player.is_dead() or player.fleeing:
            return self.fail()
        return self.success()

    def success(self):
        msg = []
        msg.append(random.choice(["Successful adventure!", "Great success!"]))
        msg += self.player.gain_exp(self.player.exp_reward() * 3)
        single_newline(msg)

        return msg

    def fail(self):
        self.player.fleeing = False
        return random.choice(
            ["The adventure was an embarassing failure.", "Failed adventure!"]
        )
