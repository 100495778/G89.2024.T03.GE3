import json
from attributes2.att_roomkey import RoomKey
from .hotel_management_exception import HotelManagementException
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from datetime import datetime
from uc3m_travel.storage.checkout_store import CheckOutStore

class HotelExit():

        def __init__(self,roomkey):
            self.__room_key = roomkey

        @property
        def room_key(self):
                """Returns the sha256 signature of the date"""
                return self.__room_key

        @room_key.setter
        def departure(self, value):
                """returns the value of the departure date"""
                self.__room_key = value


        def guest_checkout(self):
                RoomKey(self.__room_key).validate(self.__room_key)
                # check thawt the roomkey is stored in the checkins file

                out_json = CheckOutStore()
                out_json.add_item(self.__room_key)
                out_json.save_list_to_file()
                return True


