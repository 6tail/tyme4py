# -*- coding:utf-8 -*-
import unittest

from tyme4py.festival import LunarFestival
from tyme4py.lunar import LunarDay


class TestLunarFestival(unittest.TestCase):
    def test2(self):
        f = LunarFestival.from_index(2023, 0)
        assert f
        assert f.next(13).__str__() == '农历甲辰年正月初一 春节'
        assert f.next(-3).__str__() == '农历壬寅年十一月廿九 冬至节'

    def test3(self):
        f = LunarFestival.from_index(2023, 0)
        assert f
        assert f.next(-9).__str__() == '农历壬寅年三月初五 清明节'

    def test4(self):
        f = LunarDay(2010, 1, 15).get_festival()
        assert f
        assert f.__str__() == '农历庚寅年正月十五 元宵节'

    def test5(self):
        f = LunarDay(2021, 12, 29).get_festival()
        assert f
        assert f.__str__() == '农历辛丑年十二月廿九 除夕'
