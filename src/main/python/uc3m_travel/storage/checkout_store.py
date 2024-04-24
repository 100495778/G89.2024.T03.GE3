from .jsonstore import JSonStore
from ..hotel_management_config import JSON_FILES_PATH
from ..hotel_management_exception import HotelManagementException


class CheckOutStore(JSonStore):

    def __init__(self):
        file_store = file_store = JSON_FILES_PATH + "store_check_out.json"
        super().__init__(file_store)

    def add_item(self, room_key):
        reservation_found = self.find_item("room_key", room_key)
        if reservation_found:
            raise HotelManagementException("Guest is already out")

        super().add_item({"room_key":room_key})

