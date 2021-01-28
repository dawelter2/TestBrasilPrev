from board_game.property import Property


def setup_game():
    properties = list()
    properties.append(Property(150, 15))
    properties.append(Property(200, 25))
    properties.append(Property(250, 30))
    properties.append(Property(180, 20))
    properties.append(Property(90, 9))
    properties.append(Property(500, 50))
    properties.append(Property(120, 40))
    properties.append(Property(90, 8))
    properties.append(Property(200, 40))
    properties.append(Property(900, 100))
    properties.append(Property(55, 10))
    properties.append(Property(300, 20))
    properties.append(Property(450, 50))
    properties.append(Property(60, 9))
    properties.append(Property(100, 30))
    properties.append(Property(150, 30))
    properties.append(Property(90, 20))
    properties.append(Property(300, 80))
    properties.append(Property(95, 10))
    properties.append(Property(250, 60))
    assert len(properties) == 20

    return properties
