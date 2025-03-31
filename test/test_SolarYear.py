# -*- coding:utf-8 -*-
import unittest

from tyme4py.solar import SolarYear


class TestSolarYear(unittest.TestCase):
    def test0(self):
        assert SolarYear(2023).get_name() == '2023年'

    def test1(self):
        assert SolarYear(2023).is_leap() is False

    def test2(self):
        assert SolarYear(1500).is_leap() is True

    def test3(self):
        assert SolarYear(1700).is_leap() is False

    def test4(self):
        assert SolarYear(2023).get_day_count() == 365

    def test5(self):
        assert SolarYear(2023).next(5).get_name() == '2028年'

    def test6(self):
        assert SolarYear(2023).next(-5).get_name() == '2018年'
