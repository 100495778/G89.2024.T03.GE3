"""Module for the hotel manager"""
#import re
import json
from datetime import datetime
from python.attributes2.att_arrival import ArrivalDate
from python.attributes2.att_creditcard import CreditCard
from python.attributes2.att_dni import Dni
from python.attributes2.att_localizer import Localizer
from python.attributes2.att_namesurname import NameSurname
from python.attributes2.att_numdays import NumDays
from python.attributes2.att_phonenumber import PhoneNumber
from python.attributes2.att_roomkey import RoomKey
from python.attributes2.att_roomtype import RoomType
from python.uc3m_travel.hotel_management_exception import HotelManagementException
from python.uc3m_travel.hotel_reservation import HotelReservation
from python.uc3m_travel.hotel_stay import HotelStay
from python.uc3m_travel.hotel_management_config import JSON_FILES_PATH
from python.uc3m_travel.hotel_exit import HotelExit
from freezegun import freeze_time
from uc3m_travel.storage.jsonstore import JSonStore
from uc3m_travel.storage.reservation_store import RerservationStore
from uc3m_travel.storage.checkin_store import CheckInStore
from uc3m_travel.storage.checkout_store import CheckOutStore



class HotelManager(CreditCard, PhoneNumber, Dni, RoomType, ArrivalDate, Localizer, NumDays, RoomKey,
                   HotelStay):
    """Class with all the methods for managing reservations and stay"""
    def __init__(self):
        pass

    # pylint: disable=too-many-arguments
    def room_reservation(self,
                         credit_card:str,
                         name_surname:str,
                         id_card:str,
                         phone_number:str,
                         room_type:str,
                         arrival_date: str,
                         num_days:int)->str:
        """manges the hotel reservation: creates a reservation and saves it into a json file"""

        my_reservation = HotelReservation(id_card=id_card,
                                          credit_card_number=credit_card,
                                          name_surname=name_surname,
                                          phone_number=phone_number,
                                          room_type=room_type,
                                          arrival=arrival_date,
                                          num_days=num_days)

        json_store = RerservationStore()
        json_store.add_item(my_reservation)
        json_store.save_list_to_file()

        return my_reservation.localizer


    def guest_arrival(self, file_input:str)->str:
        """manages the arrival of a guest with a reservation"""
        #we get information
        my_id_card, my_localizer = self.read_from_input_file(file_input)

        # genero la room key para ello llamo a Hotel Stay
        my_checkin = HotelStay(idcard=my_id_card,localizer=my_localizer)

        #I store the information in the Json
        json_store = CheckInStore()
        json_store.add_item(my_checkin)
        json_store.save_list_to_file()
        return my_checkin.room_key

    def read_from_input_file(self, file_input):
        try:
            with open(file_input, "r", encoding="utf-8", newline="") as file:
                input_list = json.load(file)
        except FileNotFoundError as ex:
            raise HotelManagementException("Error: file input not found") from ex
        except json.JSONDecodeError as ex:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex
        # comprobar valores del fichero
        try:
            my_localizer = input_list["Localizer"]
            my_id_card = input_list["IdCard"]
        except KeyError as e:
            raise HotelManagementException("Error - Invalid Key in JSON") from e
        return my_id_card, my_localizer

    def guest_checkout(self, room_key):
        """Register the checkout of the guest"""
        checkout_json = CheckOutStore()
        check_out_info = {"room_key": room_key, "checkout_time": datetime.timestamp(datetime.utcnow())}

        check_out = HotelExit(room_key)
        check_out.guest_checkout()
        checkout_json.add_item(check_out_info)
        checkout_json.save_list_to_file()

        return True



