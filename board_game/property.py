

class Property:
    def __init__(self, sell_value, fee_value):
        self.sell_value: int = sell_value
        self.fee_value: int = fee_value
        self.owner = None

    @property
    def is_available_for_sale(self):
        return self.owner is None
