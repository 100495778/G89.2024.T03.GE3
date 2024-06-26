''' Class HotelStay (GE2.2) '''
from datetime import datetime
import hashlib
import json
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.hotel_management_exception import HotelManagementException
from attributes2 import att_roomkey
from attributes2.att_dni import Dni
from attributes2.att_localizer import Localizer
from .hotel_reservation import HotelReservation
class HotelStay():
    """Class for representing hotel stays"""
    def __init__(self,
                 idcard:str,
                 localizer:str):
        """constructor for HotelStay objects"""
        self.__alg = "SHA-256"
        self.__idcard = Dni(idcard).validate(idcard)
        self.__localizer = Localizer(localizer).validate(localizer)
        reservation = HotelReservation.load_reservation_from_localicer(self.__idcard, self.__localizer)
        self.__type = reservation[1]
        justnow = datetime.utcnow()
        self.__arrival = datetime.timestamp(justnow)
        #timestamp is represented in seconds.miliseconds
        #to add the number of days we must express num_days in seconds
        self.__departure = self.__arrival + (reservation[0] * 24 * 60 * 60)
        self.__room_key = hashlib.sha256(self.__signature_string().encode()).hexdigest()

        self.departure_date_timestamp = self.__departure

    def __signature_string(self):
        """Composes the string to be used for generating the key for the room"""
        return "{alg:" + self.__alg + ",typ:" + self.__type + ",localizer:" + \
            self.__localizer + ",arrival:" + str(self.__arrival) + \
            ",departure:" + str(self.__departure) + "}"

    @property
    def id_card(self):
        """Property that represents the product_id of the patient"""
        return self.__idcard

    @id_card.setter
    def id_card(self, value):
        self.__idcard = value

    @property
    def localizer(self):
        """Property that represents the order_id"""
        return self.__localizer

    @localizer.setter
    def localizer(self, value):
        self.__localizer = value

    @property
    def arrival(self):
        """Property that represents the phone number of the client"""
        return self.__arrival

    @property
    def room_key(self):
        """Returns the sha256 signature of the date"""
        return self.__room_key

    @property
    def departure(self):
        """Returns the issued at value"""
        return self.__departure

    @departure.setter
    def departure(self, value):
        """returns the value of the departure date"""
        self.__departure = value

    def __str__(self):
        json_info = {"id_card": self.__id_card,
                     "name_surname": self.__name_surname,
                     "credit_card": self.__credit_card_number,
                     "phone_number:": self.__phone_number,
                     "reservation_date": self.__reservation_date,
                     "arrival_date": self.__arrival,
                     "num_days": self.__num_days,
                     "room_type": self.__room_type,
                     }
        return "HotelReservation:" + json_info.__str__()
    def get_stay_from_roomkey(self, room_key: str)->bool:
        """manages the checkout of a guest"""
        att_roomkey.RoomKey(room_key).validate(room_key)
        #check thawt the roomkey is stored in the checkins file
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
            if room_key == item["_HotelStay__room_key"]:
                self.departure_date_timestamp = item["_HotelStay__departure"]
                found = True
        if not found:
            raise HotelManagementException ("Error: room key not found")


