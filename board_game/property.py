

class Property:
    def __init__(self, sell_value, fee_value):
        self._sell_value: int = sell_value
        self._fee_value: int = fee_value
        self.owner = None

    def is_available_for_sale(self):
        return self.owner is None

    def get_sell_value(self):
        return self._sell_value

    def get_fee_value(self):
        return self._fee_value
