
from mrpg.platform.files import save, load
from mrpg.core.creature import Creature

def create(overwrite=False, test=False):
    player = Creature()
    data = load("data/player.json")
    if test or overwrite or not data:
        if test:
            player.name  = "Tester"
            player.set_level(level = 99)
        else:
            player.name  = input("Name:")
            player.set_level(level = int(input("Level:")))
        data = player.export_data()
        save(data, "data/player.json")
    else:
        player.import_data(data)
    return player
