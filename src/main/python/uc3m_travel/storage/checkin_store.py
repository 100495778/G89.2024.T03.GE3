from .jsonstore import JSonStore
from ..hotel_management_config import JSON_FILES_PATH
from ..hotel_management_exception import HotelManagementException
class CheckInStore(JSonStore):

    def __init__(self):

        file_store = JSON_FILES_PATH + "store_check_in.json"
        super().__init__(file_store)


    def add_item(self,item):

        reservation_found = self.find_item("_HotelStay__room_key", item.localizer)
        if reservation_found:
            raise HotelManagementException("ckeckin  ya realizado")
        super().add_item(item)

