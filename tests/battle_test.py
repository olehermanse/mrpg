from mrpg.core.battle import Battle, Turn
from mrpg.core.game import new_player
from mrpg.core.event import Event
from mrpg.core.effects import Effects


def one_turn(battle, event_callback=None):
    assert battle.turn is None
    battle.turn = Turn(battle)
    printed_something = False
    for event in battle.turn.events:
        assert type(event) is Event
        messages = event.resolve()
        if event_callback:
            event_callback(battle)
        assert type(messages) is list
        for msg in messages:
            assert type(msg) is str
            assert len(msg.strip()) > 0
            printed_something = True
    assert printed_something
    battle.turn = None


def test_battle():
    """Test that battles between random AI end, and events look good"""
    for _ in range(100):  # AI is random
        a, b = new_player(), new_player()
        battle = Battle(a, b)
        while not battle.is_over():
            battle.a.ai()
            battle.b.ai()
            one_turn(battle)
        assert a.is_dead() or b.is_dead()


def test_speed():
    """Test that a player with higher speed will act first"""
    player = new_player()
    skills = player.skills.equipped.names()
    del player

    assert len(skills) > 3
    assert "Attack" in skills

    for defender_skill in skills:
        a, b = new_player(), new_player()
        a.set_level(b.level + 1)
        battle = Battle(a, b)
        a.pick_skill("Attack")
        b.pick_skill(defender_skill)
        a.current["hp"] = b.current["hp"] = 1
        one_turn(battle)
        assert a.is_alive() and not b.is_alive()
        assert not a.is_dead() and b.is_dead()


def test_burn():
    """Test that burn can damage and kill, and you can't heal with 0 mana"""
    a, b = new_player(), new_player()
    battle = Battle(a, b)

    a.pick_skill("Heal")
    b.pick_skill("Heal")
    a.current["hp"] = b.current["hp"] = 2
    a.current["mp"] = b.current["mp"] = 0

    burn = Effects.get("burn", target=a)
    burn.message = f"{a.name} was burned."
    burn.damage = 1
    burn.duration = 1
    a.add_effect(burn)

    burn = Effects.get("burn", target=b)
    burn.message = f"{b.name} was burned"
    burn.damage = 1
    burn.duration = 2
    b.add_effect(burn)

    assert a.current["hp"] == b.current["hp"] == 2
    assert a.current == b.current

    one_turn(battle)
    assert a.current["hp"] == b.current["hp"] == 1
    assert a.is_alive() and b.is_alive()

    a.pick_skill("Heal")
    b.pick_skill("Heal")
    one_turn(battle)
    assert a.is_alive() and b.is_dead()


def test_shock():
    """Test that shock correctly reduces dexterity"""
    a, b = new_player(), new_player()
    battle = Battle(a, b)
    a.pick_skill("Heal")
    b.pick_skill("Heal")
    a.current["hp"] = b.current["hp"] = 1
    a.current["mp"] = b.current["mp"] = 0
    a.add_effect(Effects.get("shock", target=a))

    # Effects don't do anything before their events are resolved:
    assert a.current["dex"] == b.current["dex"]
    assert a.current == b.current

    one_turn(battle)

    assert a.is_alive() and b.is_alive()
    assert a.current["dex"] < b.current["dex"]
    assert a.current != b.current


def test_lightning():
    """Test that lightning applies shock correctly"""
    a, b = new_player(), new_player()
    battle = Battle(a, b)
    a.set_level(b.level + 1)
    a.pick_skill("Lightning")
    b.pick_skill("Heal")
    dex = b.current["dex"]
    hp = battle.b.current["hp"]

    def check_dexterity_reduction(battle):
        assert (battle.b.current["hp"] == hp or battle.b.current["dex"] < dex)

    check_dexterity_reduction(battle)
    one_turn(battle, check_dexterity_reduction)

    assert a.is_alive() and b.is_alive()
    assert b.current["dex"] < dex < a.current["dex"]
