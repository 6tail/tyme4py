# -*- coding:utf-8 -*-
import unittest

from tyme4py.solar import SolarHalfYear


class TestSolarHalfYear(unittest.TestCase):
    def test0(self):
        assert SolarHalfYear(2023, 0).get_name() == '上半年'
        assert SolarHalfYear(2023, 0).__str__() == '2023年上半年'

    def test1(self):
        assert SolarHalfYear(2023, 1).get_name() == '下半年'
        assert SolarHalfYear(2023, 1).__str__() == '2023年下半年'

    def test2(self):
        assert SolarHalfYear(2023, 0).next(1).get_name() == '下半年'
        assert SolarHalfYear(2023, 0).next(1).__str__() == '2023年下半年'

    def test3(self):
        assert SolarHalfYear(2023, 0).next(2).get_name() == '上半年'
        assert SolarHalfYear(2023, 0).next(2).__str__() == '2024年上半年'

    def test4(self):
        assert SolarHalfYear(2023, 0).next(-2).get_name() == '上半年'
        assert SolarHalfYear(2023, 0).next(-2).__str__() == '2022年上半年'

    def test5(self):
        assert SolarHalfYear(2023, 0).next(-4).__str__() == '2021年上半年'
        assert SolarHalfYear(2023, 0).next(-3).__str__() == '2021年下半年'
