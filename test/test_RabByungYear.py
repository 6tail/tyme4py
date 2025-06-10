# -*- coding:utf-8 -*-
import unittest

from tyme4py.culture import Zodiac
from tyme4py.rabbyung import RabByungYear, RabByungElement


class TestRabByungYear(unittest.TestCase):
    def test0(self):
        y: RabByungYear = RabByungYear.from_element_zodiac(0, RabByungElement.from_name("火"), Zodiac.from_name("兔"))
        assert "第一饶迥火兔年" == y.get_name()
        assert "1027年" == y.get_solar_year().get_name()
        assert "丁卯" == y.get_sixty_cycle().get_name()
        assert 10 == y.get_leap_month()

    def test1(self):
        assert "第一饶迥火兔年" == RabByungYear.from_year(1027).get_name()

    def test2(self):
        assert "第十七饶迥铁虎年" == RabByungYear.from_year(2010).get_name()

    def test3(self):
        assert 5 == RabByungYear.from_year(2043).get_leap_month()
        assert 0 == RabByungYear.from_year(2044).get_leap_month()

    def test4(self):
        assert "第十六饶迥铁牛年" == RabByungYear.from_year(1961).get_name()
