import re
from .attribute import Attribute
from uc3m_travel import hotel_management_exception
class Dni(Attribute):
    def __init__(self, dni):
        self._validation_pattern = r'^[0-9]{8}[A-Z]{1}$'
        self._error_message = "Invalid DNI"
        self._attribute_value = dni

    """@staticmethod"""
    def validate(self, dni):
        """RETURN TRUE IF THE DNI IS RIGHT, OR FALSE IN OTHER CASE"""
        super().validate(dni)
        c = {"0": "T", "1": "R", "2": "W", "3": "A", "4": "G", "5": "M",
             "6": "Y", "7": "F", "8": "P", "9": "D", "10": "X", "11": "B",
             "12": "N", "13": "J", "14": "Z", "15": "S", "16": "Q", "17": "V",
             "18": "H", "19": "L", "20": "C", "21": "K", "22": "E"}
        v = int(dni[0:8])
        r = str(v % 23)
        if not dni[8] == c[r]:
            raise hotel_management_exception.HotelManagementException("Invalid IdCard letter")

        my_regex = re.compile(self._validation_pattern)

        if not my_regex.fullmatch(dni):
            raise hotel_management_exception.HotelManagementException("Invalid IdCard format")