# -*- coding:utf-8 -*-
import unittest

from tyme4py.solar import SolarDay


class TestPlumRainDay(unittest.TestCase):
    def test0(self):
        d = SolarDay(2024, 6, 10).get_plum_rain_day()
        assert d is None

    def test1(self):
        d = SolarDay(2024, 6, 11).get_plum_rain_day()
        assert d
        assert d.get_name() == '入梅'
        assert d.get_plum_rain().__str__() == '入梅'
        assert d.__str__() == '入梅第1天'

    def test2(self):
        d = SolarDay(2024, 7, 6).get_plum_rain_day()
        assert d
        assert d.get_name() == '出梅'
        assert d.get_plum_rain().__str__() == '出梅'
        assert d.__str__() == '出梅'

    def test3(self):
        d = SolarDay(2024, 7, 5).get_plum_rain_day()
        assert d
        assert d.get_name() == '入梅'
        assert d.get_plum_rain().__str__() == '入梅'
        assert d.__str__() == '入梅第25天'
