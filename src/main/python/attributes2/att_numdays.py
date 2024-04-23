from uc3m_travel import HotelManagementException
from .attribute import Attribute

class NumDays(Attribute):
    """Check NumDays"""
    def __init__(self, num_days):
        self._error_message = "Invalid number of days"
        self._attribute_value = self.validate(num_days)

    def validate(self,num_days):
        """validates the number of days"""
        super().validate((num_days))
        try:
            days = int(num_days)
        except ValueError as ex:
            raise HotelManagementException("Invalid num_days datatype") from ex
        if (days < 1 or days > 10):
            raise HotelManagementException("Numdays should be in the range 1-10")
        return num_days