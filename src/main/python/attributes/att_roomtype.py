import re

from .attribute import Attribute

class RoomType(Attribute):
    def __init__(self, room_type):
        self._validation_pattern = r"(SINGLE|DOUBLE|SUITE)"
        self._error_message = "Invalid room type"
        self._attribute_value = self.validate(room_type)
