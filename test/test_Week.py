# -*- coding:utf-8 -*-
import unittest

from tyme4py.solar import SolarDay, SolarWeek


class TestWeek(unittest.TestCase):
    def test0(self):
        assert SolarDay(1582, 10, 1).get_week().get_name() == '一'

    def test1(self):
        assert SolarDay(1582, 10, 15).get_week().get_name() == '五'

    def test2(self):
        assert SolarDay(2023, 10, 31).get_week().get_index() == 2

    def test3(self):
        w = SolarWeek(2023, 10, 0, 0)
        assert w.get_name() == '第一周'
        assert w.__str__() == '2023年10月第一周'

    def test5(self):
        w = SolarWeek(2023, 10, 4, 0)
        assert w.get_name() == '第五周'
        assert w.__str__() == '2023年10月第五周'

    def test6(self):
        w = SolarWeek(2023, 10, 5, 1)
        assert w.get_name() == '第六周'
        assert w.__str__() == '2023年10月第六周'

    def test7(self):
        w = SolarWeek(2023, 10, 0, 0).next(4)
        assert w.get_name() == '第五周'
        assert w.__str__() == '2023年10月第五周'

    def test8(self):
        w = SolarWeek(2023, 10, 0, 0).next(5)
        assert w.get_name() == '第二周'
        assert w.__str__() == '2023年11月第二周'

    def test9(self):
        w = SolarWeek(2023, 10, 0, 0).next(-1)
        assert w.get_name() == '第五周'
        assert w.__str__() == '2023年9月第五周'

    def test10(self):
        w = SolarWeek(2023, 10, 0, 0).next(-5)
        assert w.get_name() == '第一周'
        assert w.__str__() == '2023年9月第一周'

    def test11(self):
        w = SolarWeek(2023, 10, 0, 0).next(-6)
        assert w.get_name() == '第四周'
        assert w.__str__() == '2023年8月第四周'

    def test12(self):
        assert SolarDay(1582, 10, 1).get_week().get_index() == 1

    def test13(self):
        assert SolarDay(1582, 10, 15).get_week().get_index() == 5

    def test14(self):
        assert SolarDay(1129, 11, 17).get_week().get_index() == 0

    def test15(self):
        assert SolarDay(1129, 11, 1).get_week().get_index() == 5

    def test16(self):
        assert SolarDay(8, 11, 1).get_week().get_index() == 4

    def test17(self):
        assert SolarDay(1582, 9, 30).get_week().get_index() == 0

    def test18(self):
        assert SolarDay(1582, 1, 1).get_week().get_index() == 1

    def test19(self):
        assert SolarDay(1500, 2, 29).get_week().get_index() == 6

    def test20(self):
        assert SolarDay(9865, 7, 26).get_week().get_index() == 3

    def test21(self):
        start = 0
        week: SolarWeek = SolarWeek(2024, 2, 2, start)
        assert week.__str__() == '2024年2月第三周'
        assert week.get_index_in_year() == 6
        week = SolarDay(2024, 2, 11).get_solar_week(start)
        assert week.__str__() == '2024年2月第三周'
        week = SolarDay(2024, 2, 17).get_solar_week(start)
        assert week.__str__() == '2024年2月第三周'
        week = SolarDay(2024, 2, 10).get_solar_week(start)
        assert week.__str__() == '2024年2月第二周'
        week = SolarDay(2024, 2, 18).get_solar_week(start)
        assert week.__str__() == '2024年2月第四周'

    def test22(self):
        start: int = 0
        week: SolarWeek = SolarDay(2024, 7, 1).get_solar_week(start)
        assert week.__str__(), '2024年7月第一周'
        assert week.get_index_in_year() == 26
        week = week.next(1)
        assert week.__str__() == '2024年7月第二周'
