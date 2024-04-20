import re
from .attribute import Attribute


class PhoneNumber(Attribute):
    def __init__(self, attribute_value):
        self._validation_pattern = r"^(\+)[0-9]{9}"
        self._error_message = "Invalid credit card"
        self._attribute_value = self.validate(attribute_value)
