import re
from uc3m_travel import hotel_management_exception
from .attribute import Attribute


class CreditCard(Attribute):
    """CredictCard Check"""
    def __init__(self, attribute_value):
        self._validation_pattern = r"^[0-9]{16}"
        self._error_message = "Invalid credit card format"
        self._attribute_value = self.validate(attribute_value)

    def validate(self, cardnumber):
        """validates the credit card number using luhn altorithm"""
        #taken form
        # https://allwin-raju-12.medium.com/
        # credit-card-number-validation-using-luhns-algorithm-in-python-c0ed2fac6234
        # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE GUID
        # RETURN TRUE IF THE GUID IS RIGHT, OR FALSE IN OTHER CASE
        super().validate(cardnumber)
        myregex = re.compile(self._validation_pattern)
        regex_check = myregex.fullmatch(cardnumber)
        if not regex_check:
            raise hotel_management_exception.HotelManagementException(self._error_message)
        def digits_of(n):
            return [int(d) for d in str(n)]


        digits = digits_of(cardnumber)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        if not checksum % 10 == 0:
            raise hotel_management_exception.HotelManagementException("Invalid credit card number (not luhn)")
        return cardnumber