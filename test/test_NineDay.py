# -*- coding:utf-8 -*-
import unittest

from tyme4py.solar import SolarDay


class TestNineDay(unittest.TestCase):
    def test(self):
        d = SolarDay(2020, 12, 21).get_nine_day()
        assert d
        assert d.get_name() == '一九'
        assert d.get_nine().__str__() == '一九'
        assert d.__str__() == '一九第1天'

    def test1(self):
        d = SolarDay(2020, 12, 22).get_nine_day()
        assert d
        assert d.get_name() == '一九'
        assert d.get_nine().__str__() == '一九'
        assert d.__str__() == '一九第2天'

    def test2(self):
        d = SolarDay(2020, 1, 7).get_nine_day()
        assert d
        assert d.get_name() == '二九'
        assert d.get_nine().__str__() == '二九'
        assert d.__str__() == '二九第8天'

    def test3(self):
        d = SolarDay(2021, 1, 6).get_nine_day()
        assert d
        assert d.get_name() == '二九'
        assert d.get_nine().__str__() == '二九'
        assert d.__str__() == '二九第8天'

    def test4(self):
        d = SolarDay(2021, 1, 8).get_nine_day()
        assert d
        assert d.get_name() == '三九'
        assert d.get_nine().__str__() == '三九'
        assert d.__str__() == '三九第1天'

    def test5(self):
        d = SolarDay(2021, 3, 5).get_nine_day()
        assert d
        assert d.get_name() == '九九'
        assert d.get_nine().__str__() == '九九'
        assert d.__str__() == '九九第3天'

    def test6(self):
        d = SolarDay(2021, 7, 5).get_nine_day()
        assert d is None
