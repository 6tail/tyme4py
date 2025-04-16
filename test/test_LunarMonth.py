# -*- coding:utf-8 -*-
import unittest

from tyme4py.lunar import LunarMonth, LunarDay
from tyme4py.solar import SolarDay


class TestLunarMonth(unittest.TestCase):
    def test0(self):
        assert LunarMonth.from_ym(2359, 7).get_name() == '七月'

    def test1(self):
        """闰月"""
        assert LunarMonth.from_ym(2359, -7).get_name() == '闰七月'

    def test2(self):
        assert LunarMonth.from_ym(2023, 6).get_day_count() == 29

    def test3(self):
        assert LunarMonth.from_ym(2023, 7).get_day_count() == 30

    def test4(self):
        assert LunarMonth.from_ym(2023, 8).get_day_count() == 30

    def test5(self):
        assert LunarMonth.from_ym(2023, 9).get_day_count() == 29

    def test6(self):
        assert LunarMonth.from_ym(2023, 9).get_first_julian_day().get_solar_day().__str__() == '2023年10月15日'

    def test7(self):
        assert LunarMonth.from_ym(2023, 1).get_sixty_cycle().get_name() == '甲寅'

    def test8(self):
        assert LunarMonth.from_ym(2023, -2).get_sixty_cycle().get_name() == '丙辰'

    def test9(self):
        assert LunarMonth.from_ym(2023, 3).get_sixty_cycle().get_name() == '丁巳'

    def test10(self):
        assert LunarMonth.from_ym(2024, 1).get_sixty_cycle().get_name() == '丙寅'

    def test11(self):
        assert LunarMonth.from_ym(2023, 12).get_sixty_cycle().get_name() == '丙寅'

    def test12(self):
        assert LunarMonth.from_ym(2022, 1).get_sixty_cycle().get_name() == '壬寅'

    def test13(self):
        assert LunarMonth.from_ym(37, -12).get_name() == '闰十二月'

    def test14(self):
        assert LunarMonth.from_ym(5552, -12).get_name() == '闰十二月'

    def test15(self):
        assert LunarMonth.from_ym(2008, 11).next(1).__str__() == '农历戊子年十二月'

    def test16(self):
        assert LunarMonth.from_ym(2008, 11).next(2).__str__() == '农历己丑年正月'

    def test17(self):
        assert LunarMonth.from_ym(2008, 11).next(6).__str__() == '农历己丑年五月'

    def test18(self):
        assert LunarMonth.from_ym(2008, 11).next(7).__str__() == '农历己丑年闰五月'

    def test19(self):
        assert LunarMonth.from_ym(2008, 11).next(8).__str__() == '农历己丑年六月'

    def test20(self):
        assert LunarMonth.from_ym(2008, 11).next(15).__str__() == '农历庚寅年正月'

    def test21(self):
        assert LunarMonth.from_ym(2008, 12).next(-1).__str__() == '农历戊子年十一月'

    def test22(self):
        assert LunarMonth.from_ym(2009, 1).next(-2).__str__() == '农历戊子年十一月'

    def test23(self):
        assert LunarMonth.from_ym(2009, 5).next(-6).__str__() == '农历戊子年十一月'

    def test24(self):
        assert LunarMonth.from_ym(2009, -5).next(-7).__str__() == '农历戊子年十一月'

    def test25(self):
        assert LunarMonth.from_ym(2009, 6).next(-8).__str__() == '农历戊子年十一月'

    def test26(self):
        assert LunarMonth.from_ym(2010, 1).next(-15).__str__() == '农历戊子年十一月'

    def test27(self):
        assert LunarMonth.from_ym(2012, -4).get_day_count() == 29

    def test28(self):
        assert LunarMonth.from_ym(2023, 9).get_sixty_cycle().__str__() == '癸亥'

    def test29(self):
        d: LunarDay = SolarDay(2023, 10, 7).get_lunar_day()
        assert d.get_lunar_month().get_sixty_cycle().__str__() == '壬戌'
        assert d.get_sixty_cycle_day().get_month().__str__() == '辛酉'

    def test30(self):
        d: LunarDay = SolarDay(2023, 10, 8).get_lunar_day()
        assert d.get_lunar_month().get_sixty_cycle().__str__() == '壬戌'
        assert d.get_sixty_cycle_day().get_month().__str__() == '壬戌'

    def test31(self):
        d: LunarDay = SolarDay(2023, 10, 15).get_lunar_day()
        assert d.get_lunar_month().get_name() == '九月'
        assert d.get_lunar_month().get_sixty_cycle().__str__() == '癸亥'
        assert d.get_sixty_cycle_day().get_month().__str__() == '壬戌'

    def test32(self):
        d: LunarDay = SolarDay(2023, 11, 7).get_lunar_day()
        assert d.get_lunar_month().get_sixty_cycle().__str__() == '癸亥'
        assert d.get_sixty_cycle_day().get_month().__str__() == '壬戌'

    def test33(self):
        d: LunarDay = SolarDay(2023, 11, 8).get_lunar_day()
        assert d.get_lunar_month().get_sixty_cycle().__str__() == '癸亥'
        assert d.get_sixty_cycle_day().get_month().__str__() == '癸亥'

    def test34(self):
        # 2023年闰2月
        m: LunarMonth = LunarMonth.from_ym(2023, 12)
        assert m.__str__() == '农历癸卯年十二月'
        assert m.next(-1).__str__() == '农历癸卯年十一月'
        assert m.next(-2).__str__() == '农历癸卯年十月'

    def test35(self):
        # 2023年闰2月
        m: LunarMonth = LunarMonth.from_ym(2023, 3)
        assert m.__str__() == '农历癸卯年三月'
        assert m.next(-1).__str__() == '农历癸卯年闰二月'
        assert m.next(-2).__str__() == '农历癸卯年二月'
        assert m.next(-3).__str__() == '农历癸卯年正月'
        assert m.next(-4).__str__() == '农历壬寅年十二月'
        assert m.next(-5).__str__() == '农历壬寅年十一月'

    def test36(self):
        d: LunarDay = SolarDay(1983, 2, 15).get_lunar_day()
        assert d.get_lunar_month().get_sixty_cycle().__str__() == '甲寅'
        assert d.get_sixty_cycle_day().get_month().__str__() == '甲寅'

    def test37(self):
        d: LunarDay = SolarDay(2023, 10, 30).get_lunar_day()
        assert d.get_lunar_month().get_sixty_cycle().__str__() == '癸亥'
        assert d.get_sixty_cycle_day().get_month().__str__() == '壬戌'

    def test38(self):
        d: LunarDay = SolarDay(2023, 10, 19).get_lunar_day()
        assert d.get_lunar_month().get_sixty_cycle().__str__() == '癸亥'
        assert d.get_sixty_cycle_day().get_month().__str__() == '壬戌'

    def test39(self):
        m: LunarMonth = LunarMonth.from_ym(2023, 11)
        assert m.__str__() == '农历癸卯年十一月'
        assert m.get_sixty_cycle().__str__() == '乙丑'

    def test40(self):
        assert LunarMonth.from_ym(2018, 6).get_sixty_cycle().__str__() == '己未'

    def test41(self):
        assert LunarMonth.from_ym(2017, 12).get_sixty_cycle().__str__() == '甲寅'

    def test42(self):
        assert LunarMonth.from_ym(2018, 1).get_sixty_cycle().__str__() == '甲寅'

    def test43(self):
        assert LunarDay(2018, 6, 26).get_sixty_cycle_day().get_month().__str__() == '庚申'
