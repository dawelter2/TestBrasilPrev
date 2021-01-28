import random
from abc import ABC, abstractmethod


class RoundLimitExceeded(Exception):
    pass


class Player(ABC):
    def __init__(self):
        self.money = 300
        self.properties = []
        self.round_count = 0
        self.last_property_landed = 0

    def is_alive(self) -> bool:
        return self.money > 0 and self.round_count < 1000

    def new_round(self):
        self.money += 100
        self.round_count += 1
        if self.round_count >= 1000:
            raise RoundLimitExceeded("The round limit was exceeded, ending the game.")

    @abstractmethod
    def should_buy_property(self, property_value, fee_value) -> bool:
        pass


class Impulsive(Player):
    def __init__(self):
        super().__init__()

    def should_buy_property(self, property_value, fee_value) -> bool:
        if self.money > property_value:
            return True
        return False


class Demanding(Player):
    def __init__(self):
        super().__init__()

    def should_buy_property(self, property_value, fee_value) -> bool:
        if self.money > property_value and fee_value > 50:
            return True
        return False


class Cautious(Player):
    def __init__(self):
        super().__init__()

    def should_buy_property(self, property_value, fee_value) -> bool:
        if self.money - property_value >= 80:
            return True
        return False


class Random(Player):
    def __init__(self):
        super().__init__()

    def should_buy_property(self, property_value, fee_value) -> bool:
        if self.money > property_value and random.randint(0, 1):
            return True
        return False
