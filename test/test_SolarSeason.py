# -*- coding:utf-8 -*-
import unittest

from tyme4py.solar import SolarSeason


class TestSolatSeason(unittest.TestCase):
    def test0(self):
        season: SolarSeason = SolarSeason(2023, 0)
        assert season.__str__() == '2023年一季度'
        assert season.next(-5).__str__() == '2021年四季度'
        assert season.next(5).__str__() == '2024年二季度'
