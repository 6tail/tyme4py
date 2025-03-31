# -*- coding:utf-8 -*-
import unittest

from tyme4py.solar import SolarDay


class TestConstellation(unittest.TestCase):
    def test(self):
        assert SolarDay(2020, 3, 21).get_constellation().get_name() == '白羊'
        assert SolarDay(2020, 4, 19).get_constellation().get_name() == '白羊'

    def test1(self):
        assert SolarDay(2020, 4, 20).get_constellation().get_name() == '金牛'
        assert SolarDay(2020, 5, 20).get_constellation().get_name() == '金牛'

    def test2(self):
        assert SolarDay(2020, 5, 21).get_constellation().get_name() == '双子'
        assert SolarDay(2020, 6, 21).get_constellation().get_name() == '双子'

    def test3(self):
        assert SolarDay(2020, 6, 22).get_constellation().get_name() == '巨蟹'
        assert SolarDay(2020, 7, 22).get_constellation().get_name() == '巨蟹'
