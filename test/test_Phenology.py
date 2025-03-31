# -*- coding:utf-8 -*-
import unittest

from tyme4py.solar import SolarDay


class TestPhenology(unittest.TestCase):
    def test0(self):
        solar_day = SolarDay(2020, 4, 23)
        # 七十二候
        phenology = solar_day.get_phenology_day()
        # 三候
        three_phenology = phenology.get_phenology().get_three_phenology()
        assert solar_day.get_term().get_name() == '谷雨'
        assert three_phenology.get_name() == '初候'
        assert phenology.get_name() == '萍始生'
        # 该候的第5天
        assert phenology.get_day_index() == 4

    def test1(self):
        solar_day = SolarDay(2021, 12, 26)
        # 七十二候
        phenology = solar_day.get_phenology_day()
        # 三候
        three_phenology = phenology.get_phenology().get_three_phenology()
        assert solar_day.get_term().get_name() == '冬至'
        assert three_phenology.get_name() == '二候'
        assert phenology.get_name() == '麋角解'
        # 该候的第1天
        assert phenology.get_day_index() == 0
