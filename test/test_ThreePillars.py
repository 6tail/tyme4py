# -*- coding:utf-8 -*-
import unittest

from tyme4py.sixtycycle import ThreePillars
from tyme4py.solar import SolarDay


class TestThreePillars(unittest.TestCase):
    def test(self):
        t: ThreePillars = ThreePillars('甲戌', '甲戌', '甲戌')
        day_list: [str] = []
        for d in t.get_solar_days(1, 2200):
            day_list.append(d.__str__())
        assert day_list == [
            '14年10月17日',
            '194年11月1日',
            '254年10月17日',
            '434年11月1日',
            '494年10月17日',
            '674年11月1日',
            '734年10月17日',
            '794年10月2日',
            '974年10月17日',
            '1034年10月2日',
            '1214年10月17日',
            '1274年10月2日',
            '1454年10月17日',
            '1514年10月2日',
            '1694年10月27日',
            '1754年10月13日',
            '1934年10月30日',
            '1994年10月15日',
            '2174年10月31日'
        ]

    def test1(self):
        assert SolarDay.from_ymd(1034, 10, 2).get_sixty_cycle_day().get_three_pillars().get_name() == '甲戌 甲戌 甲戌'
