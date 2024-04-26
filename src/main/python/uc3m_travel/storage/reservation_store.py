from .jsonstore import JSonStore
from ..hotel_management_config import JSON_FILES_PATH
from ..hotel_management_exception import HotelManagementException
class RerservationStore(JSonStore):

    def __init__(self):

        file_store = file_store = JSON_FILES_PATH + "store_reservation.json"
        super().__init__(file_store)


    def add_item(self,item):
        reservation_found = self.find_item("_HotelReservation__localizer",item.localizer)
        if reservation_found:
            raise HotelManagementException("Reservation already exists")

        reservation_found = self.find_item("_HotelReservation__id_card", item.id_card)
        if reservation_found:
            raise HotelManagementException("This ID card has another reservation")

        super().add_item(item)