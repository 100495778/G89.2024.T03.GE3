import unittest
import csv
import json
import os.path
import shutil
import hashlib
from unittest import TestCase
from os import remove
from freezegun import freeze_time
from uc3m_travel import (JSON_FILES_PATH,
                         JSON_FILES_GUEST_ARRIVAL,
                         HotelManager,
                         HotelManagementException)
from attributes2.att_dni import Dni
class TestSingletonHotelManager(unittest.TestCase):
    def test_singleton_hotel_manager(self):
        access_manager_1 = HotelManager()
        access_manager_2 = HotelManager()
        access_manager_3 = HotelManager()

        self.assertEqual(access_manager_1, access_manager_2)
        self.assertEqual(access_manager_2, access_manager_3)
        self.assertEqual(access_manager_3, access_manager_1) # add assertion here

        # we try now 2 classes that do not have a singleton
        dni1 = Dni("12345678Z")
        dni2 = Dni("12345678Z")
        self.assertNotEqual(dni1, dni2)



