from mrpg.core.battle import Battle, Turn
from mrpg.core.game import new_player
from mrpg.core.event import Event


def test_battle():
    """Test that battles between random AI end, and events look good"""
    for _ in range(100):  # AI is random
        a, b = new_player(), new_player()
        battle = Battle(a, b)
        while not battle.is_over():
            battle.a.ai()
            battle.b.ai()
            battle.turn = Turn(battle)
            printed_something = False
            for event in battle.turn.events:
                assert type(event) is Event
                messages = event.apply()
                assert type(messages) is list
                # assert len(messages) > 0
                for msg in messages:
                    assert type(msg) is str
                    assert len(msg.strip()) > 0
                    printed_something = True
            assert printed_something
            battle.turn = None
