from decimal import Decimal

class Dict_FloatsToDecimals():

    def __init__(self):
        pass
    
    def recursive_float_to_decimal(self, dict_item):
        for key, value in dict_item.items():
            if type(value) is dict:
                self.recursive_float_to_decimal(value)
            elif type(value) is list:
                for dictionary in value:
                    self.recursive_float_to_decimal(dictionary)
            else:
                if isinstance(value, float):
                    dict_item[key] = Decimal(value)
