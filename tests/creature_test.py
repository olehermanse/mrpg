from mrpg.core.creature import Creature


def test_creature():
    c = Creature("Tester", 2)
    assert c.name == "Tester"
    assert c.level == 2


def test_creature_level():
    c = Creature("Tester", 2)
    hp = c.base["hp"]
    msg = c.gain_exp(10000)
    assert c.level > 2
    assert c.base["hp"] > hp
    assert msg
    for m in msg:
        print(m)
        assert type(m) is str


def test_creature_skills():
    c = Creature("Fighter", 11)
    skills = ["attack", "heal"]
    c.skills.learn(skills)
    res = c.skills.learned.names()
    hints = c.skills.learned.hints()
    assert len(res) == len(skills) and len(hints) == len(skills)
    for a, b in zip(skills, res):
        assert a.lower() == b.lower()


def test_creature_damage():
    c = Creature("Fighter", 11)
    msg = c.damage(c.current["hp"] - 1)
    for o in c.limit_check():
        o.apply()

    assert msg
    assert len(msg) > 0
    assert c.is_alive()
    msg = c.damage(1)
    for o in c.limit_check():
        o.apply()
    assert msg
    assert len(msg) > 0
    assert not c.is_alive()


def test_creature_restore():
    c = Creature("Fighter", 11)
    msg = []
    msg += c.damage(c.current["hp"])
    msg += c.restore(1)
    for o in c.limit_check():
        o.apply()

    assert msg
    assert len(msg) >= 2
    assert c.is_alive()
    assert c.current["hp"] == 1


def test_creature_export():
    j = Creature("Jason", 42)
    data = j.export_data()
    i = Creature("Tester", 22)
    i.import_data(data)
    assert i.name == j.name
    assert i.level == j.level
    assert i.base["hp"] == j.base["hp"]
    for key in j.base:
        print(key)
        assert key in i.base
        assert i.base[key] == j.base[key]
