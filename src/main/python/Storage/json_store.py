import json
import datetime
from uc3m_travel import hotel_management_exception
from uc3m_travel import hotel_management_config


class JsonStore:
    """This class takes the file and the  information we want to store"""
    def __init__(self):
        self._path = hotel_management_config.JSON_FILES_PATH

    def save_reservation (self, reservation_info):

        file_store = self._path + "store_reservation.json"

        # leo los datos del fichero si existe , y si no existe creo una lista vacia
        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            data_list = []
        except json.JSONDecodeError as ex:
            raise hotel_management_exception.HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex

        # compruebo que esta reserva no esta en la lista
        for item in data_list:
            if reservation_info.localizer == item["_HotelReservation__localizer"]:
                raise hotel_management_exception.HotelManagementException("Reservation already exists")
            if reservation_info.id_card == item["_HotelReservation__id_card"]:
                raise hotel_management_exception.HotelManagementException("This ID card has another reservation")
        # añado los datos de mi reserva a la lista , a lo que hubiera
        data_list.append(reservation_info.__dict__)

        # escribo la lista en el fichero
        try:
            with open(file_store, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise hotel_management_exception.HotelManagementException("Wrong file  or file path") from ex

        return reservation_info.localizer

    def save_checkin(self, my_checkin):

        file_store = self._path + "store_check_in.json"

        # leo los datos del fichero si existe , y si no existe creo una lista vacia
        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                room_key_list = json.load(file)
        except FileNotFoundError as ex:
            room_key_list = []
        except json.JSONDecodeError as ex:
            raise hotel_management_exception.HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex

        # comprobar que no he hecho otro ckeckin antes
        for item in room_key_list:
            if my_checkin.room_key == item["_HotelStay__room_key"]:
                raise hotel_management_exception.HotelManagementException("ckeckin  ya realizado")

        # añado los datos de mi reserva a la lista , a lo que hubiera
        room_key_list.append(my_checkin.__dict__)

        try:
            with open(file_store, "w", encoding="utf-8", newline="") as file:
                json.dump(room_key_list, file, indent=2)
        except FileNotFoundError as ex:
            raise hotel_management_exception.HotelManagementException("Wrong file  or file path") from ex

        return my_checkin.room_key

    def save_checkout(self, room_key):

        file_store_checkout = self._path + "store_check_out.json"
        try:
            with open(file_store_checkout, "r", encoding="utf-8", newline="") as file:
                room_key_list = json.load(file)
        except FileNotFoundError as ex:
            room_key_list = []
        except json.JSONDecodeError as ex:
            raise hotel_management_exception.HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex

        for checkout in room_key_list:
            if checkout["room_key"] == room_key:
                raise hotel_management_exception.HotelManagementException("Guest is already out")

        room_checkout = {"room_key": room_key, "checkout_time": datetime.timestamp(datetime.utcnow())}

        room_key_list.append(room_checkout)

        try:
            with open(file_store_checkout, "w", encoding="utf-8", newline="") as file:
                json.dump(room_key_list, file, indent=2)
        except FileNotFoundError as ex:
            raise hotel_management_exception.HotelManagementException("Wrong file  or file path") from ex




