from .attribute import Attribute
import re

class NameSurname(Attribute):
    def __init__(self, name_surname):
        self._validation_pattern = r"^(?=^.{10,50}$)([a-zA-Z]+(\s[a-zA-Z]+)+)$"
        self._error_message = "Invalid name format"
        self._attribute_value = self.validate(name_surname)