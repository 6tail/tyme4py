# -*- coding:utf-8 -*-
import unittest

from tyme4py.solar import SolarDay


class TestSixStar(unittest.TestCase):
    def test0(self):
        assert SolarDay(2020, 4, 23).get_lunar_day().get_six_star().get_name(), '佛灭'

    def test1(self):
        assert SolarDay(2021, 1, 15).get_lunar_day().get_six_star().get_name() == '友引'

    def test2(self):
        assert SolarDay(2017, 1, 5).get_lunar_day().get_six_star().get_name() == '先胜'

    def test3(self):
        assert SolarDay(2020, 4, 10).get_lunar_day().get_six_star().get_name() == '友引'

    def test4(self):
        assert SolarDay(2020, 6, 11).get_lunar_day().get_six_star().get_name() == '大安'

    def test5(self):
        assert SolarDay(2020, 6, 1).get_lunar_day().get_six_star().get_name() == '先胜'

    def test6(self):
        assert SolarDay(2020, 12, 8).get_lunar_day().get_six_star().get_name() == '先负'

    def test8(self):
        assert SolarDay(2020, 12, 11).get_lunar_day().get_six_star().get_name() == '赤口'
