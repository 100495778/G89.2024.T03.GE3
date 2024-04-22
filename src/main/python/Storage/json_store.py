import json
import hotel_management_exception
import hotel_management_config


class JsonStore ():
    """This class takes the file and the  information we want to store"""
    def __init__(self):

    def checkout_json(self, room_info):

        file_store = hotel_management_config.JSON_FILES_PATH + "store_reservation.json"

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
            if room_info.localizer == item["_HotelReservation__localizer"]:
                raise hotel_management_exception.HotelManagementException("Reservation already exists")
            if room_info.id_card == item["_HotelReservation__id_card"]:
                raise hotel_management_exception.HotelManagementException("This ID card has another reservation")
        # añado los datos de mi reserva a la lista , a lo que hubiera
        data_list.append(room_info.__dict__)

        # escribo la lista en el fichero
        try:
            with open(file_store, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise hotel_management_exception.HotelManagementException("Wrong file  or file path") from ex

        return room_info.localizer



