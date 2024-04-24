import json
from attributes2.att_roomkey import RoomKey
from .hotel_management_exception import HotelManagementException
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from Storage import json_store
from datetime import datetime

class Hotel_exit():

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
                file_store = JSON_FILES_PATH + "store_check_in.json"
                try:
                        with open(file_store, "r", encoding="utf-8", newline="") as file:
                                room_key_list = json.load(file)
                except FileNotFoundError as ex:
                        raise HotelManagementException("Error: store checkin not found") from ex
                except json.JSONDecodeError as ex:
                        raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex

                # comprobar que esa room_key es la que me han dado
                found = False
                for item in room_key_list:
                        if self.__room_key == item["_HotelStay__room_key"]:
                                departure_date_timestamp = item["_HotelStay__departure"]
                                found = True
                if not found:
                        raise HotelManagementException("Error: room key not found")

                today = datetime.utcnow().date()
                if datetime.fromtimestamp(departure_date_timestamp).date() != today:
                        raise HotelManagementException("Error: today is not the departure day")

                file_store_checkout = JSON_FILES_PATH + "store_check_out.json"

                json_store.JsonStore().save_checkout(self.__room_key)
                return True

                """try:
                        with open(file_store_checkout, "r", encoding="utf-8", newline="") as file:
                                room_key_list = json.load(file)
                except FileNotFoundError as ex:
                        room_key_list = []
                except json.JSONDecodeError as ex:
                        raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex

                for checkout in room_key_list:
                        if checkout["room_key"] == self._room_key:
                                raise HotelManagementException("Guest is already out")

                room_checkout = {"room_key": self._room_key, "checkout_time": datetime.timestamp(datetime.utcnow())}

                room_key_list.append(room_checkout)

                try:
                        with open(file_store_checkout, "w", encoding="utf-8", newline="") as file:
                                json.dump(room_key_list, file, indent=2)
                except FileNotFoundError as ex:
                        raise HotelManagementException("Wrong file  or file path") from ex

                return True"""
