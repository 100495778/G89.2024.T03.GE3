from uc3m_travel import hotel_management_exception
from .attribute import Attribute

class NumDays(Attribute):
    """Check NumDays"""
    def __init__(self, num_days):
        self._error_message = "Invalid number of days"
        self._attribute_value = self.validate(num_days)

    def validate(self,num_days):
        """validates the number of days"""
        try:
            days = int(num_days)
        except ValueError as ex:
            raise hotel_management_exception.HotelManagementException("Invalid num_days datatype") from ex
        if days < 1 or days > 10:
            raise hotel_management_exception.HotelManagementException("Numdays should be in the range 1-10")
        return num_days
