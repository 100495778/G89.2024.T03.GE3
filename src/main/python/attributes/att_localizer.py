import re
from .attribute import Attribute

class Localizer(Attribute):
    """Check Localizer"""
    def __init__(self, localizer):
        self._validation_pattern = r'^[a-fA-F0-9]{32}$'
        self._error_message = "Invalid localizer"
        self._attribute_value = self.validate(localizer)
