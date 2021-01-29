from board_game.property import Property


def test_property():
    property = Property(10, 1)
    assert property.is_available_for_sale

    property.owner = "Fake Player"
    assert not property.is_available_for_sale
