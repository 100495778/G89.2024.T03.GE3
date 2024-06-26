from .jsonstore import JSonStore
from ..hotel_management_config import JSON_FILES_PATH
from ..hotel_management_exception import HotelManagementException


class CheckOutStore(JSonStore):

    def __init__(self):
        file_store = JSON_FILES_PATH + "store_check_out.json"
        self.__data_list = []
        super().__init__(file_store)

    def add_item(self, check_out):

        reservation_found = self.find_item("_HotelExit__room_key", check_out.room_key)
        if reservation_found:
            raise HotelManagementException("Guest is already out")

        #self.__data_list.append(check_out)
        super().add_item(check_out)

