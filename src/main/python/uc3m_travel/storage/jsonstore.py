import json
from uc3m_travel.hotel_management_exception import HotelManagementException
from ..hotel_management_config import JSON_FILES_PATH

class JSonStore():
    __file_name = ""
    __data_list = []

    def __init__(self,file_name):
        self.__file_name = file_name
        self.__data_list = []
        self.load_list_from_file()

    def save_list_to_file(self):
        # escribo la lista en el fichero
        print(self.__data_list)
        try:
            with open(self.__file_name, "w", encoding="utf-8", newline="") as file:
                json.dump(self.__data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise HotelManagementException("Wrong file  or file path") from ex

    def add_item(self, my_reservation):
        # añado los datos de mi reserva a la lista , a lo que hubiera
        self.__data_list.append(my_reservation.__dict__)

    def find_item(self, key , value):
        # compruebo que esta reserva no esta en la lista
        for item in self.__data_list:
            if item[key] == value:
                return item
        return None
    def load_list_from_file(self):
        # escribo el fichero Json con todos los datos

        # llamo a JsonStore para guardar la reserva
        # json_store.JsonStore().save_reservation(my_reservation)
        # leo los datos del fichero si existe , y si no existe creo una lista vacia
        try:
            with open(self.__file_name, "r", encoding="utf-8", newline="") as file:
                self.__data_list = json.load(file)
        except FileNotFoundError:
            self.__data_list = []
        except json.JSONDecodeError as ex:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex

