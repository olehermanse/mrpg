from mrpg.core.battle import Battle
from mrpg.core.adventure import get_monster, fail_message
from mrpg.ui.terminal import clear, menu, fancy_print
from mrpg.utils import column_string


def start_adventure(player):
    for _ in range(3):
        enemy = get_monster(player)
        clear()
        fancy_print("You encounter a {}".format(enemy.string_short()))
        winner = battle_loop(player, enemy)
        if not player.is_alive():
            return "dead"
        if not winner:
            clear()
            fancy_print(fail_message())
            return "fail"
        clear()
        fancy_print("Victory, you defeated {}.".format(enemy.name))
        fancy_print(player.gain_exp(enemy.exp_reward()))

    clear()
    fancy_print("Successful adventure!")
    fancy_print(player.gain_exp(200))
    return "success"


def battle_loop(player, enemy):
    battle = Battle(player, enemy)
    while True:
        a = player.string_long().split(sep="\n")
        b = enemy.string_long().split(sep="\n")

        clear()
        print(column_string("| ", a, " | ", b, " |"))
        print()
        skill_names = player.skills.equipped.names()
        skill_hints = player.skills.equipped.hints()
        choice = menu(
            "Battle Menu:", lst=skill_names, hints=skill_hints, f="flee")

        if choice == "flee":
            fancy_print("{} fled like a big coward.".format(player.name))
            break
        if choice not in skill_names:
            assert False

        player.use_skill = player.skills.equipped.get(choice)
        enemy.use_skill = enemy.skills.equipped.get(0)

        results = battle.resolve_turn()
        fancy_print("\n".join(results))
        if enemy.is_alive() and player.is_alive():
            continue
        else:
            break
    if player.is_alive() and enemy.is_alive():
        return None
    if enemy.is_alive():
        return enemy
    if player.is_alive():
        return player
    return None
