import re

from uc3m_travel import HotelManagementException
from .attribute import Attribute


class CreditCard(Attribute):
    def __init__(self, attribute_value):
        self._validation_pattern = r"^[0-9]{16}"
        self._error_message = "Invalid credit card"
        self._attribute_value = self.validate(attribute_value)

    def validate( self, x ):
        """validates the credit card number using luhn altorithm"""
        #taken form
        # https://allwin-raju-12.medium.com/
        # credit-card-number-validation-using-luhns-algorithm-in-python-c0ed2fac6234
        # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE GUID
        # RETURN TRUE IF THE GUID IS RIGHT, OR FALSE IN OTHER CASE
        myregex = re.compile(self._validation_pattern)
        regex_check = myregex.fullmatch(x)
        if not regex_check:
            raise HotelManagementException(self._error_message)
        def digits_of(n):
            return [int(d) for d in str(n)]


        digits = digits_of(x)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        if not checksum % 10 == 0:
            raise HotelManagementException("Invalid credit card number (not luhn)")
        return x