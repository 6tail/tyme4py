# -*- coding:utf-8 -*-
import unittest

from tyme4py.solar import SolarDay


class TestDirection(unittest.TestCase):
    def test(self):
        assert SolarDay(2021, 11, 13).get_lunar_day().get_sixty_cycle().get_heaven_stem().get_mascot_direction().get_name() == '东南'

    def test1(self):
        assert SolarDay(2024, 1, 1).get_lunar_day().get_sixty_cycle().get_heaven_stem().get_mascot_direction().get_name() == '东南'

    def test2(self):
        assert SolarDay(2023, 11, 6).get_lunar_day().get_jupiter_direction().get_name() == '东'
