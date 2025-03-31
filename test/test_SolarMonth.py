# -*- coding:utf-8 -*-
import unittest

from tyme4py.solar import SolarMonth


class TestSolarMonth(unittest.TestCase):
    def test0(self):
        m = SolarMonth(2019, 5)
        assert m.get_name() == '5月'
        assert m.__str__() == '2019年5月'

    def test1(self):
        m = SolarMonth(2023, 1)
        assert m.get_week_count(0) == 5
        assert m.get_week_count(1) == 6
        assert m.get_week_count(2) == 6
        assert m.get_week_count(3) == 5
        assert m.get_week_count(4) == 5
        assert m.get_week_count(5) == 5
        assert m.get_week_count(6) == 5

    def test2(self):
        m = SolarMonth(2023, 2)
        assert m.get_week_count(0) == 5
        assert m.get_week_count(1) == 5
        assert m.get_week_count(2) == 5
        assert m.get_week_count(3) == 4
        assert m.get_week_count(4) == 5
        assert m.get_week_count(5) == 5
        assert m.get_week_count(6) == 5

    def test3(self):
        m = SolarMonth(2023, 10).next(1)
        assert m.get_name() == '11月'
        assert m.__str__() == '2023年11月'

    def test4(self):
        m = SolarMonth(2023, 10)
        assert m.next(2).__str__() == '2023年12月'
        assert m.next(3).__str__() == '2024年1月'
        assert m.next(-5).__str__() == '2023年5月'
        assert m.next(-9).__str__() == '2023年1月'
        assert m.next(-10).__str__() == '2022年12月'
        assert m.next(24).__str__() == '2025年10月'
        assert m.next(-24).__str__() == '2021年10月'
