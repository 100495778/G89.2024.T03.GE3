from json_store import JsonStore

class Reservation(JsonStore):
    """Store of Reservation"""
    def __init__(self,path,room_info):
        super().__init__(path)
        self._room_info = room_info

    def save_reservation(self):
        super().save_reservation(self._room_info)
