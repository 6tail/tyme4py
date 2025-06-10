# -*- coding:utf-8 -*-
import unittest

from tyme4py.culture import Zodiac
from tyme4py.rabbyung import RabByungDay, RabByungElement
from tyme4py.solar import SolarDay


class TestRabByungDay(unittest.TestCase):
    def test0(self):
        # 测试公历1951年1月8日转换为藏历日
        solar_day = SolarDay.from_ymd(1951, 1, 8)
        rab_day = RabByungDay.from_solar_day(solar_day)
        self.assertEqual("第十六饶迥铁虎年十二月初一", str(rab_day))

        # 测试藏历日转换为公历日
        rab_day2 = RabByungDay.from_element_zodiac(15, RabByungElement.from_name("铁"), Zodiac.from_name("虎"), 12, 1)
        self.assertEqual("1951年1月8日", str(rab_day2.get_solar_day()))

    def test1(self):
        # 测试公历2051年2月11日转换为藏历日
        solar_day = SolarDay.from_ymd(2051, 2, 11)
        rab_day = RabByungDay.from_solar_day(solar_day)
        self.assertEqual("第十八饶迥铁马年十二月三十", str(rab_day))

        # 测试藏历日转换为公历日
        rab_day2 = RabByungDay.from_element_zodiac(17, RabByungElement.from_name("铁"), Zodiac.from_name("马"), 12, 30)
        self.assertEqual("2051年2月11日", str(rab_day2.get_solar_day()))

    def test2(self):
        # 测试公历2025年4月23日转换为藏历日
        solar_day = SolarDay.from_ymd(2025, 4, 23)
        rab_day = RabByungDay.from_solar_day(solar_day)
        self.assertEqual("第十七饶迥木蛇年二月廿五", str(rab_day))

        # 测试藏历日转换为公历日
        rab_day2 = RabByungDay.from_element_zodiac(16, RabByungElement.from_name("木"), Zodiac.from_name("蛇"), 2, 25)
        self.assertEqual("2025年4月23日", str(rab_day2.get_solar_day()))

    def test3(self):
        # 测试公历1951年2月8日转换为藏历日
        solar_day = SolarDay.from_ymd(1951, 2, 8)
        rab_day = RabByungDay.from_solar_day(solar_day)
        self.assertEqual("第十六饶迥铁兔年正月初二", str(rab_day))

        # 测试藏历日转换为公历日
        rab_day2 = RabByungDay.from_element_zodiac(15, RabByungElement.from_name("铁"), Zodiac.from_name("兔"), 1, 2)
        self.assertEqual("1951年2月8日", str(rab_day2.get_solar_day()))

    def test4(self):
        # 测试公历1951年1月24日转换为藏历日（闰日）
        solar_day = SolarDay.from_ymd(1951, 1, 24)
        rab_day = RabByungDay.from_solar_day(solar_day)
        self.assertEqual("第十六饶迥铁虎年十二月闰十六", str(rab_day))

        # 测试藏历日转换为公历日（闰日）
        rab_day2 = RabByungDay.from_element_zodiac(15, RabByungElement.from_name("铁"), Zodiac.from_name("虎"), 12, -16)
        self.assertEqual("1951年1月24日", str(rab_day2.get_solar_day()))

    def test5(self):
        # 测试公历1961年6月24日转换为藏历日
        solar_day = SolarDay.from_ymd(1961, 6, 24)
        rab_day = RabByungDay.from_solar_day(solar_day)
        self.assertEqual("第十六饶迥铁牛年五月十一", str(rab_day))

        # 测试藏历日转换为公历日
        rab_day2 = RabByungDay.from_element_zodiac(15, RabByungElement.from_name("铁"), Zodiac.from_name("牛"), 5, 11)
        self.assertEqual("1961年6月24日", str(rab_day2.get_solar_day()))

    def test6(self):
        # 测试公历1952年2月23日转换为藏历日
        solar_day = SolarDay.from_ymd(1952, 2, 23)
        rab_day = RabByungDay.from_solar_day(solar_day)
        self.assertEqual("第十六饶迥铁兔年十二月廿八", str(rab_day))

        # 测试藏历日转换为公历日
        rab_day2 = RabByungDay.from_element_zodiac(15, RabByungElement.from_name("铁"), Zodiac.from_name("兔"), 12, 28)
        self.assertEqual("1952年2月23日", str(rab_day2.get_solar_day()))

    def test7(self):
        # 测试公历2025年4月26日转换为藏历日
        solar_day = SolarDay.from_ymd(2025, 4, 26)
        rab_day = RabByungDay.from_solar_day(solar_day)
        self.assertEqual("第十七饶迥木蛇年二月廿九", str(rab_day))

    def test8(self):
        # 测试公历2025年4月25日转换为藏历日
        solar_day = SolarDay.from_ymd(2025, 4, 25)
        rab_day = RabByungDay.from_solar_day(solar_day)
        self.assertEqual("第十七饶迥木蛇年二月廿七", str(rab_day))
