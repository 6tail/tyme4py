# -*- coding:utf-8 -*-
import unittest

from tyme4py.solar import SolarDay


class TestEcliptic(unittest.TestCase):
    def test(self):
        star = SolarDay(2023, 10, 30).get_lunar_day().get_twelve_star()
        assert star.get_name() == '天德'
        assert star.get_ecliptic().get_name() == '黄道'
        assert star.get_ecliptic().get_luck().get_name() == '吉'

    def test1(self):
        star = SolarDay(2023, 10, 19).get_lunar_day().get_twelve_star()
        assert star.get_name() == '白虎'
        assert star.get_ecliptic().get_name() == '黑道'
        assert star.get_ecliptic().get_luck().get_name() == '凶'

    def test2(self):
        star = SolarDay(2023, 10, 7).get_lunar_day().get_twelve_star()
        assert star.get_name() == '天牢'
        assert star.get_ecliptic().get_name() == '黑道'
        assert star.get_ecliptic().get_luck().get_name() == '凶'

    def test3(self):
        star = SolarDay(2023, 10, 8).get_lunar_day().get_twelve_star()
        assert star.get_name() == '玉堂'
        assert star.get_ecliptic().get_name() == '黄道'
        assert star.get_ecliptic().get_luck().get_name() == '吉'
