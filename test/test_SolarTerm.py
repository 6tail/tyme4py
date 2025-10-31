# -*- coding:utf-8 -*-
import unittest

from tyme4py.solar import SolarTerm, SolarDay


class TestSolarTerm(unittest.TestCase):
    def test0(self):
        # 冬至在去年，2022 - 12 - 22 05: 48:11
        dong_zhi = SolarTerm(2023, '冬至')
        assert dong_zhi.get_name() == '冬至'
        assert dong_zhi.get_index() == 0
        # 公历日
        assert dong_zhi.get_julian_day().get_solar_day().__str__() == '2022年12月22日'
        assert dong_zhi.get_solar_day().__str__() == '2022年12月22日'

        # 冬至顺推23次，就是大雪 2023 - 12 - 07 17: 32:55
        daXue = dong_zhi.next(23)
        assert daXue.get_name() == '大雪'
        assert daXue.get_index() == 23
        assert daXue.get_julian_day().get_solar_day().__str__() == '2023年12月7日'
        assert daXue.get_solar_day().__str__() == '2023年12月7日'

        # 冬至逆推2次，就是上一年的小雪 2022 - 11 - 22 16: 20:28
        xiaoXue = dong_zhi.next(-2)
        assert xiaoXue.get_name() == '小雪'
        assert xiaoXue.get_index() == 22
        assert xiaoXue.get_julian_day().get_solar_day().__str__() == '2022年11月22日'
        assert xiaoXue.get_solar_day().__str__() == '2022年11月22日'

        # 冬至顺推24次，就是下一个冬至 2023 - 12 - 22 11: 27:20
        dong_zhi2 = dong_zhi.next(24)
        assert dong_zhi2.get_name() == '冬至'
        assert dong_zhi2.get_index() == 0
        assert dong_zhi2.get_julian_day().get_solar_day().__str__() == '2023年12月22日'
        assert dong_zhi2.get_solar_day().__str__() == '2023年12月22日'

    def test1(self):
        # 公历2023年的雨水，2023 - 02 - 19 06: 34:16
        jq = SolarTerm(2023, '雨水')
        assert jq.get_name() == '雨水'
        assert jq.get_index() == 4

    def test2(self):
        # 公历2023年的大雪，2023 - 12 - 07 17: 32:55
        jq = SolarTerm(2023, '大雪')
        assert jq.get_name() == '大雪'
        # 索引
        assert jq.get_index() == 23
        # 公历
        assert jq.get_julian_day().get_solar_day().__str__() == '2023年12月7日'
        assert jq.get_solar_day().__str__() == '2023年12月7日'
        # 农历
        assert jq.get_julian_day().get_solar_day().get_lunar_day().__str__() == '农历癸卯年十月廿五'
        # 推移
        assert jq.next(5).get_name() == '雨水'

    def test3(self):
        assert SolarDay(2023, 10, 10).get_term().get_name() == '寒露'

    def test4(self):
        assert SolarDay(2023, 12, 7).get_term_day().__str__() == '大雪第1天'
        assert SolarDay(2023, 12, 7).get_term_day().get_day_index() == 0

        assert SolarDay(2023, 12, 8).get_term_day().__str__() == '大雪第2天'
        assert SolarDay(2023, 12, 21).get_term_day().__str__() == '大雪第15天'

        assert SolarDay(2023, 12, 22).get_term_day().__str__() == '冬至第1天'

    def test5(self):
        assert SolarTerm.from_name(1034, '寒露').get_solar_day().__str__() == '1034年10月1日'
        assert SolarTerm.from_name(1034, '寒露').get_julian_day().get_solar_day().__str__() == '1034年10月3日'
        assert SolarTerm.from_name(1034, '寒露').get_julian_day().get_solar_time().__str__() == '1034年10月3日 06:02:28'
