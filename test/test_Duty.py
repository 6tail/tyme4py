# -*- coding:utf-8 -*-
import unittest

from tyme4py.solar import SolarDay


class TestDuty(unittest.TestCase):
    def test(self):
        assert SolarDay(2023, 10, 30).get_lunar_day().get_duty().get_name() == '闭'

    def test1(self):
        assert SolarDay(2023, 10, 19).get_lunar_day().get_duty().get_name() == '建'

    def test2(self):
        assert SolarDay(2023, 10, 7).get_lunar_day().get_duty().get_name() == '除'

    def test3(self):
        assert SolarDay(2023, 10, 8).get_lunar_day().get_duty().get_name() == '除'
