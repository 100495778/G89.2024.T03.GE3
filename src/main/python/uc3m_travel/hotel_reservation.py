"""Hotel reservation class"""
import hashlib
from datetime import datetime
from uc3m_travel.storage.reservation_store import RerservationStore
from uc3m_travel.hotel_management_exception import HotelManagementException
from freezegun import freeze_time
from python.attributes2.att_arrival import ArrivalDate
from python.attributes2.att_creditcard import CreditCard
from python.attributes2.att_dni import Dni
from python.attributes2.att_localizer import Localizer
from python.attributes2.att_namesurname import NameSurname
from python.attributes2.att_numdays import NumDays
from python.attributes2.att_phonenumber import PhoneNumber
from python.attributes2.att_roomkey import RoomKey
from python.attributes2.att_roomtype import RoomType


class HotelReservation:
    """Class for representing hotel reservations"""
    #pylint: disable=too-many-arguments, too-many-instance-attributes
    def __init__(self,
                 id_card:str,
                 credit_card_number:str,
                 name_surname:str,
                 phone_number:str,
                 room_type:str,
                 arrival:str,
                 num_days:int):
        """constructor of reservation objects"""
        self.__credit_card_number = CreditCard(credit_card_number).attribute_value
        self.__id_card = Dni(id_card).attribute_value
        justnow = datetime.utcnow()
        self.__arrival = ArrivalDate(arrival).attribute_value
        self.__reservation_date = datetime.timestamp(justnow)
        self.__name_surname = NameSurname(name_surname).attribute_value
        self.__phone_number = PhoneNumber(phone_number).attribute_value
        self.__room_type = RoomType(room_type).attribute_value
        self.__num_days = NumDays(num_days).attribute_value
        self.__localizer =  hashlib.md5(str(self).encode()).hexdigest()

    def __str__(self):
        """return a json string with the elements required to calculate the localizer"""
        #VERY IMPORTANT: JSON KEYS CANNOT BE RENAMED
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
    @property
    def credit_card(self):
        """property for getting and setting the credit_card number"""
        return self.__credit_card_number
    @credit_card.setter
    def credit_card(self, value):
        self.__credit_card_number = value

    @property
    def id_card(self):
        """property for getting and setting the id_card"""
        return self.__id_card
    @id_card.setter
    def id_card(self, value):
        self.__id_card = value

    @property
    def room_type(self):
        """property for getting and setting the roomtype"""
        return self.__room_type

    @property
    def num_days(self):
        """property for getting and setting the roomtype"""
        return self.__num_days




    @property
    def localizer(self):
        """Returns the md5 signature"""
        return self.__localizer

    @classmethod
    def load_reservation_from_localicer(self, my_id_card, my_localizer):
        # debe existir para hacer el checkin
        reservation_store = RerservationStore()
        reservation = reservation_store.find_item("_HotelReservation__localizer", my_localizer)
        if not reservation:
            raise HotelManagementException("Error: localizer not found")
        reservation = reservation_store.find_item("_HotelReservation__id_card", my_id_card)
        if not reservation:
            raise HotelManagementException("Error: idcard not found")

        reservation_days = reservation["_HotelReservation__num_days"]
        reservation_room_type = reservation["_HotelReservation__room_type"]
        reservation_date_timestamp = reservation["_HotelReservation__reservation_date"]
        reservation_credit_card = reservation["_HotelReservation__credit_card_number"]
        reservation_date_arrival = reservation["_HotelReservation__arrival"]
        reservation_name = reservation["_HotelReservation__name_surname"]
        reservation_phone = reservation["_HotelReservation__phone_number"]
        reservation_id_card = reservation["_HotelReservation__id_card"]

        # regenrar clave y ver si coincide
        reservation_date = datetime.fromtimestamp(reservation_date_timestamp)
        with freeze_time(reservation_date):
            new_reservation = HotelReservation(credit_card_number=reservation_credit_card,
                                               id_card=reservation_id_card,
                                               num_days=reservation_days,
                                               room_type=reservation_room_type,
                                               arrival=reservation_date_arrival,
                                               name_surname=reservation_name,
                                               phone_number=reservation_phone)
        if new_reservation.localizer != my_localizer:
            raise HotelManagementException("Error: reservation has been manipulated")
        # compruebo si hoy es la fecha de checkin
        reservation_format = "%d/%m/%Y"
        date_obj = datetime.strptime(reservation_date_arrival, reservation_format)
        if date_obj.date() != datetime.date(datetime.utcnow()):
            raise HotelManagementException("Error: today is not reservation date")
        return reservation_days, reservation_room_type
