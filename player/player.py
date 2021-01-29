import random
from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self):
        self.money = 300
        self.properties = []
        self.round_counter = 0
        self.last_property_landed = 0

    @property
    def is_alive(self) -> bool:
        """
        Return true if the player should keep playing
        """
        return self.money >= 0

    def new_round(self):
        """
        Give money to player each time he reaches the end of the board.
        """
        self.money += 100

    @abstractmethod
    def should_buy_property(self, property_value, fee_value) -> bool:
        """
        Each player must implement their game style.
        :param property_value: The value to buy a property.
        :param fee_value: The fee value its property will pay.
        :return: True if should buy, false if not.
        """
        pass


class Impulsive(Player):
    def __init__(self):
        super().__init__()

    def should_buy_property(self, property_value, fee_value) -> bool:
        if self.money >= property_value:
            return True
        return False


class Demanding(Player):
    def __init__(self):
        super().__init__()

    def should_buy_property(self, property_value, fee_value) -> bool:
        if self.money >= property_value and fee_value > 50:
            return True
        return False


class Cautious(Player):
    def __init__(self):
        super().__init__()

    def should_buy_property(self, property_value, fee_value) -> bool:
        if self.money - property_value >= 80:
            return True
        return False


def randint(a, b):
    """This method was created to be easier to mock in tests"""
    return random.randint(a, b)


class Random(Player):
    def __init__(self):
        super().__init__()

    def should_buy_property(self, property_value, fee_value) -> bool:
        if self.money >= property_value and randint(0, 1):
            return True
        return False
