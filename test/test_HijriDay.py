# -*- coding:utf-8 -*-
import unittest

from tyme4py.hijri import HijriDay
from tyme4py.solar import SolarDay


class TestHijriDay(unittest.TestCase):
    def test0(self):
        assert SolarDay.from_ymd(622, 7, 16).get_hijri_day().__str__() == '1年穆哈兰姆月1日'

    def test1(self):
        assert SolarDay.from_ymd(2026, 5, 13).get_hijri_day().__str__() == '1447年都尔喀尔德月26日'
        assert HijriDay.from_ymd(1447, 11, 26).get_solar_day().__str__() == '2026年5月13日'

    def test2(self):
        assert SolarDay.from_ymd(100, 7, 8).get_hijri_day().__str__() == '-538年都尔黑哲月12日'
        assert HijriDay.from_ymd(-538, 12, 12).get_solar_day().__str__() == '100年7月8日'

    def test3(self):
        assert SolarDay.from_ymd(622, 7, 15).get_hijri_day().__str__() == '0年都尔黑哲月29日'
        assert HijriDay.from_ymd(0, 12, 29).get_solar_day().__str__() == '622年7月15日'

    def test4(self):
        assert SolarDay.from_ymd(1, 1, 1).get_hijri_day().__str__() == '-640年主马达·敖外鲁月16日'
        assert HijriDay.from_ymd(-640, 5, 16).get_solar_day().__str__() == '1年1月1日'

    def test5(self):
        assert SolarDay.from_ymd(9999, 12, 31).get_hijri_day().__str__() == '9666年赖比尔·阿色尼月2日'
        assert HijriDay.from_ymd(9666, 4, 2).get_solar_day().__str__() == '9999年12月31日'
