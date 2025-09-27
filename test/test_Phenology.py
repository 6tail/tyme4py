# -*- coding:utf-8 -*-
import unittest

from tyme4py.culture.phenology import Phenology
from tyme4py.solar import SolarDay, SolarTime


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

    def test2(self):
        p = Phenology.from_index(2026, 1)
        jd = p.get_julian_day()
        assert p.get_name() == '麋角解'
        assert jd.get_solar_day().__str__() == '2025年12月26日'
        assert jd.get_solar_time().__str__() == '2025年12月26日 20:49:56'

    def test3(self):
        p = SolarDay.from_ymd(2025, 12, 26).get_phenology()
        jd = p.get_julian_day()
        assert p.get_name() == '麋角解'
        assert jd.get_solar_day().__str__() == '2025年12月26日'
        assert jd.get_solar_time().__str__() == '2025年12月26日 20:49:56'

    def test4(self):
        assert SolarTime.from_ymd_hms(2025, 12, 26, 20, 49, 38).get_phenology().get_name() == '蚯蚓结'
        assert SolarTime.from_ymd_hms(2025, 12, 26, 20, 49, 56).get_phenology().get_name() == '麋角解'
