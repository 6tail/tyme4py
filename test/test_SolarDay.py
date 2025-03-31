# -*- coding:utf-8 -*-
import unittest

from tyme4py.solar import SolarDay


class TestSolarDay(unittest.TestCase):
    def test0(self):
        assert SolarDay(2023, 1, 1).get_name() == '1日'
        assert SolarDay(2023, 1, 1).__str__() == '2023年1月1日'

    def test1(self):
        assert SolarDay(2000, 2, 29).get_name() == '29日'
        assert SolarDay(2000, 2, 29).__str__() == '2000年2月29日'

    def test2(self):
        assert SolarDay(2023, 1, 1).get_index_in_year() == 0
        assert SolarDay(2023, 12, 31).get_index_in_year() == 364
        assert SolarDay(2020, 12, 31).get_index_in_year() == 365

    def test3(self):
        assert SolarDay(2023, 1, 1).subtract(SolarDay(2023, 1, 1)) == 0
        assert SolarDay(2023, 1, 2).subtract(SolarDay(2023, 1, 1)) == 1
        assert SolarDay(2023, 1, 1).subtract(SolarDay(2023, 1, 2)) == -1
        assert SolarDay(2023, 2, 1).subtract(SolarDay(2023, 1, 1)) == 31
        assert SolarDay(2023, 1, 1).subtract(SolarDay(2023, 2, 1)) == -31
        assert SolarDay(2024, 1, 1).subtract(SolarDay(2023, 1, 1)) == 365
        assert SolarDay(2023, 1, 1).subtract(SolarDay(2024, 1, 1)) == -365
        assert SolarDay(1582, 10, 15).subtract(SolarDay(1582, 10, 4)) == 1

    def test4(self):
        assert SolarDay(1582, 10, 15).next(-1).__str__() == '1582年10月4日'

    def test5(self):
        assert SolarDay(2000, 2, 28).next(2).__str__() == '2000年3月1日'

    def test6(self):
        assert SolarDay(2020, 5, 24).get_lunar_day().__str__() == '农历庚子年闰四月初二'

    def test7(self):
        assert SolarDay(2020, 5, 24).subtract(SolarDay(2020, 4, 23)) == 31

    def test8(self):
        assert SolarDay(16, 11, 30).get_lunar_day().__str__() == '农历丙子年十一月十二'

    def test9(self):
        assert SolarDay(2023, 10, 27).get_term().__str__() == '霜降'

    def test10(self):
        assert SolarDay(2023, 10, 27).get_phenology_day().__str__() == '豺乃祭兽第4天'

    def test11(self):
        assert SolarDay(2023, 10, 27).get_phenology_day().get_phenology().get_three_phenology().__str__() == '初候'

    def test22(self):
        assert '甲辰' == SolarDay(2024, 2, 10).get_lunar_day().get_lunar_month().get_lunar_year().get_sixty_cycle().get_name()

    def test23(self):
        assert '癸卯' == SolarDay(2024, 2, 9).get_lunar_day().get_lunar_month().get_lunar_year().get_sixty_cycle().get_name()
