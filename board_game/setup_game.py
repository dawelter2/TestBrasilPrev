from board_game.property import Property


def setup_game():
    properties = list()
    properties.append(Property(150, 30))
    properties.append(Property(200, 50))
    properties.append(Property(250, 60))
    properties.append(Property(180, 45))
    properties.append(Property(90, 15))
    properties.append(Property(500, 200))
    properties.append(Property(120, 30))
    properties.append(Property(90, 20))
    properties.append(Property(200, 45))
    properties.append(Property(900, 300))
    properties.append(Property(55, 10))
    properties.append(Property(300, 100))
    properties.append(Property(450, 150))
    properties.append(Property(60, 5))
    properties.append(Property(100, 40))
    properties.append(Property(150, 60))
    properties.append(Property(90, 40))
    properties.append(Property(300, 80))
    properties.append(Property(95, 15))
    properties.append(Property(250, 50))
    assert len(properties) == 20

    return properties
