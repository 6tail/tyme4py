# -*- coding:utf-8 -*-
import unittest

from tyme4py.solar import SolarDay


class TestJulianDay(unittest.TestCase):
    def test(self):
        assert SolarDay(2023, 1, 1).get_julian_day().get_solar_day().__str__() == '2023年1月1日'
