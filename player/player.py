

class Player:
    def __init__(self):
        self.money = 300
        self.properties = []

    def is_alive(self):
        return self.money > 0

    def new_round(self):
        self.money += 100
