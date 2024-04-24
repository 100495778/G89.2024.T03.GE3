import re
from .attribute import Attribute


class RoomKey(Attribute):
    """Check Room Key"""
    def __init__(self, roomkey):
        self._validation_pattern = r'^[a-fA-F0-9]{64}$'
        self._error_message = "Invalid room key format"
        self._attribute_value = self.validate(roomkey)
