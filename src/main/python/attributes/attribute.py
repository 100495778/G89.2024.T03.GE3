from python.uc3m_travel.hotel_management_exception import HotelManagementException
import re

class Attribute():
    def __init__(self):
        self._validation_pattern = r""
        self._error_message = ""
        self._attribute_value = ""

    def validate(self, attribute_value):
        myregex = re.compile(self._validation_pattern)
        regex_check = myregex.fullmatch(attribute_value)
        if not regex_check:
            raise HotelManagementException(self._error_message)
        return attribute_value
