# -*- coding:utf-8 -*-
import unittest

from tyme4py.lunar import LunarHour, LunarDay, LunarMonth, LunarYear
from tyme4py.solar import SolarDay


class TestNineStar(unittest.TestCase):
    def test0(self):
        nine_star = LunarYear(1985).get_nine_star()
        assert nine_star.get_name() == '六'
        assert nine_star.__str__() == '六白金'

    def test1(self):
        nine_star = LunarYear(2022).get_nine_star()
        assert nine_star.__str__() == '五黄土'
        assert nine_star.get_dipper().__str__() == '玉衡'

    def test2(self):
        nine_star = LunarYear(2033).get_nine_star()
        assert nine_star.__str__() == '三碧木'
        assert nine_star.get_dipper().__str__() == '天玑'

    def test3(self):
        nine_star = LunarMonth.from_ym(1985, 2).get_nine_star()
        assert nine_star.__str__() == '四绿木'
        assert nine_star.get_dipper().__str__() == '天权'

    def test4(self):
        nine_star = LunarMonth.from_ym(1985, 2).get_nine_star()
        assert nine_star.__str__() == '四绿木'
        assert nine_star.get_dipper().__str__() == '天权'

    def test5(self):
        nine_star = LunarMonth.from_ym(2022, 1).get_nine_star()
        assert nine_star.__str__() == '二黑土'
        assert nine_star.get_dipper().__str__() == '天璇'

    def test6(self):
        nine_star = LunarMonth.from_ym(2033, 1).get_nine_star()
        assert nine_star.__str__() == '五黄土'
        assert nine_star.get_dipper().__str__() == '玉衡'

    def test7(self):
        nine_star = SolarDay(1985, 2, 19).get_lunar_day().get_nine_star()
        assert nine_star.__str__() == '五黄土'
        assert nine_star.get_dipper().__str__() == '玉衡'

    def test8(self):
        nine_star = LunarDay(2022, 1, 1).get_nine_star()
        assert nine_star.__str__() == '四绿木'
        assert nine_star.get_dipper().__str__() == '天权'

    def test9(self):
        nine_star = LunarDay(2033, 1, 1).get_nine_star()
        assert nine_star.__str__() == '一白水'
        assert nine_star.get_dipper().__str__() == '天枢'

    def test10(self):
        nine_star = LunarHour(2033, 1, 1, 12, 0, 0).get_nine_star()
        assert nine_star.__str__() == '七赤金'
        assert nine_star.get_dipper().__str__() == '摇光'

    def test11(self):
        nine_star = LunarHour(2011, 5, 3, 23, 0, 0).get_nine_star()
        assert nine_star.__str__() == '七赤金'
        assert nine_star.get_dipper().__str__() == '摇光'
