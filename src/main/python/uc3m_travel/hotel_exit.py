import json
from attributes2.att_roomkey import RoomKey
from uc3m_travel.hotel_management_exception import HotelManagementException
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

        def __str__(self):
                json_info = {"room_key": self.__room_key,
                             "checkout_time": datetime.timestamp(datetime.utcnow())
                             }
                return "HotelCheckout:" + json_info.__str__()


        def guest_checkout(self):
                checkin_store = CheckInStore()

                file_store = JSON_FILES_PATH + "store_check_in.json"
                try:
                        with open(file_store, "r", encoding="utf-8", newline="") as file:
                                room_key_list = json.load(file)
                except FileNotFoundError as ex:
                        raise HotelManagementException("Error: store checkin not found") from ex
                except json.JSONDecodeError as ex:
                        raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex

                # check thawt the roomkey is stored in the checkins file
                reservation = checkin_store.find_item("_HotelStay__room_key", self.__room_key)
                if not reservation:
                        raise HotelManagementException("Error: room key not found")

                for item in room_key_list:
                        if self.__room_key == item["_HotelStay__room_key"]:
                                departure_date_timestamp = item["_HotelStay__departure"]


                today = datetime.utcnow().date()
                if datetime.fromtimestamp(departure_date_timestamp).date() != today:
                        raise HotelManagementException("Error: today is not the departure day")










