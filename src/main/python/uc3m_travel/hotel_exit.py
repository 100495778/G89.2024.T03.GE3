import json
from attributes2.att_roomkey import RoomKey
from .hotel_management_exception import HotelManagementException
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from datetime import datetime
from uc3m_travel.storage.checkout_store import CheckOutStore
from uc3m_travel.storage.checkin_store import CheckInStore

class HotelExit:

        def __init__(self,roomkey):
            self.__room_key = RoomKey(roomkey).validate(roomkey)

        @property
        def room_key(self):
                """Returns the sha256 signature of the date"""
                return self.__room_key


        def guest_checkout(self):
                checkout_json = CheckOutStore()
                checkin_store = CheckInStore()
                # check thawt the roomkey is stored in the checkins file
                reservation = checkin_store.find_item("_HotelStay__room_key", self.__room_key)
                if not reservation:
                        raise HotelManagementException("Error: room key not found")




