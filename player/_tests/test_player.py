from player.player import Impulsive, Demanding, Cautious, Random


def test_player():
    # instantiate Impulsive to test Player property and methods (is_alive and new_round)
    player = Impulsive()
    assert player.is_alive
    assert player.money == 300
    player.new_round()
    assert player.money == 400


def test_impulsive():
    player = Impulsive()

    # Cheap property
    assert player.should_buy_property(100, 10)
    # Expensive property
    assert player.should_buy_property(300, 30)
    # More Expensive property
    assert not player.should_buy_property(301, 30)


def test_demanding():
    player = Demanding()

    # Cheap property
    assert not player.should_buy_property(100, 10)
    # Expensive property with good fee
    assert player.should_buy_property(300, 51)
    # Expensive property with bad fee
    assert not player.should_buy_property(300, 50)
    # More Expensive property with good fee
    assert not player.should_buy_property(301, 51)


def test_cautious():
    player = Cautious()

    # Cheap property
    assert player.should_buy_property(100, 10)
    # Medium price property
    assert player.should_buy_property(220, 22)
    # Medium price property
    assert not player.should_buy_property(221, 22)
    # Expensive property
    assert not player.should_buy_property(300, 50)


def test_random(mocker):
    player = Random()

    # Mock the result to return zero (False) always
    mocker.patch("player.player.randint", return_value=0)

    # Cheap property
    assert not player.should_buy_property(100, 10)
    # Medium price property
    assert not player.should_buy_property(220, 22)
    # Expensive property
    assert not player.should_buy_property(300, 50)
    # Expensive property
    assert not player.should_buy_property(500, 50)

    # Mock the result to return one (True) always
    mocker.patch("player.player.randint", return_value=1)

    # Cheap property
    assert player.should_buy_property(100, 10)
    # Medium price property
    assert player.should_buy_property(220, 22)
    # Expensive property
    assert player.should_buy_property(300, 50)
    # Expensive property
    assert not player.should_buy_property(500, 50)
