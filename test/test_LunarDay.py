# -*- coding:utf-8 -*-
import unittest

from tyme4py.lunar import LunarDay


class TestLunarDay(unittest.TestCase):
    def test1(self):
        assert LunarDay(0, 11, 18).get_solar_day().__str__() == '1年1月1日'

    def test2(self):
        assert LunarDay(9999, 12, 2).get_solar_day().__str__() == '9999年12月31日'

    def test3(self):
        assert LunarDay(1905, 1, 1).get_solar_day().__str__() == '1905年2月4日'

    def test4(self):
        assert LunarDay(2038, 12, 29).get_solar_day().__str__() == '2039年1月23日'

    def test5(self):
        assert LunarDay(1500, 1, 1).get_solar_day().__str__() == '1500年1月31日'

    def test6(self):
        assert LunarDay(1500, 12, 29).get_solar_day().__str__() == '1501年1月18日'

    def test7(self):
        assert LunarDay(1582, 9, 18).get_solar_day().__str__() == '1582年10月4日'

    def test8(self):
        assert LunarDay(1582, 9, 19).get_solar_day().__str__() == '1582年10月15日'

    def test9(self):
        assert LunarDay(2019, 12, 12).get_solar_day().__str__() == '2020年1月6日'

    def test10(self):
        assert LunarDay(2033, -11, 1).get_solar_day().__str__() == '2033年12月22日'

    def test11(self):
        assert LunarDay(2021, 6, 7).get_solar_day().__str__() == '2021年7月16日'

    def test12(self):
        assert LunarDay(2034, 1, 1).get_solar_day().__str__() == '2034年2月19日'

    def test13(self):
        assert LunarDay(2033, 12, 1).get_solar_day().__str__() == '2034年1月20日'

    def test14(self):
        assert LunarDay(7013, -11, 4).get_solar_day().__str__() == '7013年12月24日'

    def test15(self):
        assert LunarDay(2023, 8, 24).get_sixty_cycle().__str__() == '己亥'

    def test16(self):
        assert LunarDay(1653, 1, 6).get_sixty_cycle().__str__() == '癸酉'

    def test17(self):
        assert LunarDay(2010, 1, 1).next(31).__str__() == '农历庚寅年二月初二'

    def test18(self):
        assert LunarDay(2012, 3, 1).next(60).__str__() == '农历壬辰年闰四月初一'

    def test19(self):
        assert LunarDay(2012, 3, 1).next(88).__str__() == '农历壬辰年闰四月廿九'

    def test20(self):
        assert LunarDay(2012, 3, 1).next(89).__str__() == '农历壬辰年五月初一'

    def test21(self):
        assert LunarDay(2020, 4, 1).get_solar_day().__str__() == '2020年4月23日'

    def test22(self):
        assert LunarDay(2024, 1, 1).get_lunar_month().get_lunar_year().get_sixty_cycle().get_name() == '甲辰'

    def test23(self):
        assert LunarDay(2023, 12, 30).get_lunar_month().get_lunar_year().get_sixty_cycle().get_name() == '癸卯'

    def test24(self):
        """二十八宿"""
        star = LunarDay(2020, 4, 13).get_twenty_eight_star()
        assert star.get_zone().get_name() == '南'
        assert star.get_zone().get_beast().get_name() == '朱雀'
        assert star.get_name() == '翼'
        assert star.get_seven_star().get_name() == '火'
        assert star.get_animal().get_name() == '蛇'
        assert star.get_luck().get_name() == '凶'

        assert star.get_land().get_name() == '阳天'
        assert star.get_land().get_direction().get_name() == '东南'

    def test25(self):
        star = LunarDay(2023, 9, 28).get_twenty_eight_star()
        assert star.get_zone().get_name() == '南'
        assert star.get_zone().get_beast().get_name() == '朱雀'
        assert star.get_name() == '柳'
        assert star.get_seven_star().get_name() == '土'
        assert star.get_animal().get_name() == '獐'
        assert star.get_luck().get_name() == '凶'

        assert star.get_land().get_name() == '炎天'
        assert star.get_land().get_direction().get_name() == '南'

    def test26(self):
        lunar: LunarDay = LunarDay(2005, 11, 23)
        assert lunar.get_lunar_month().get_sixty_cycle().get_name() == '戊子'
        assert lunar.get_month_sixty_cycle().get_name() == '戊子'

    def test27(self):
        lunar: LunarDay = LunarDay(2024, 1, 1)
        assert lunar.next(31).__str__() == '农历甲辰年二月初三'

    def test28(self):
        lunar: LunarDay = LunarDay(2024, 3, 5)
        assert lunar.get_minor_ren().get_name() == '大安'
