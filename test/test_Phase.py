# -*- coding(self):utf-8 -*-
import unittest

from tyme4py.culture import Phase
from tyme4py.lunar import LunarDay
from tyme4py.solar import SolarDay, SolarTime


class TestPhase(unittest.TestCase):
    
    def test0(self):
        phase = Phase.from_name(2025, 7, '下弦月')
        assert '2025年9月14日 18(self):32(self):57', phase.get_solar_time().__str__()

    def test1(self):
        phase = Phase.from_index(2025, 7, 6)
        assert '2025年9月14日 18(self):32(self):57', phase.get_solar_time().__str__()

    def test2(self):
        phase = Phase.from_index(2025, 7, 8)
        assert '2025年9月22日 03(self):54(self):07', phase.get_solar_time().__str__()

    def test3(self):
        phase = SolarDay.from_ymd(2025, 9, 21).get_phase()
        assert '残月', phase.__str__()

    def test4(self):
        phase = LunarDay.from_ymd(2025, 7, 30).get_phase()
        assert '残月', phase.__str__()

    def test5(self):
        phase = SolarTime.from_ymd_hms(2025, 9, 22, 4, 0, 0).get_phase()
        assert '蛾眉月', phase.__str__()

    def test6(self):
        phase = SolarTime.from_ymd_hms(2025, 9, 22, 3, 0, 0).get_phase()
        assert '残月', phase.__str__()

    def test7(self):
        d = SolarDay.from_ymd(2023, 9, 15).get_phase_day()
        assert '新月第1天', d.__str__()

    def test8(self):
        d = SolarDay.from_ymd(2023, 9, 17).get_phase_day()
        assert '蛾眉月第2天', d.__str__()

    def test9(self):
        phase = SolarTime.from_ymd_hms(2025, 9, 22, 3, 54, 7).get_phase()
        assert '新月', phase.__str__()

    def test10(self):
        phase = SolarTime.from_ymd_hms(2025, 9, 22, 3, 54, 6).get_phase()
        assert '残月', phase.__str__()

    def test11(self):
        phase = SolarTime.from_ymd_hms(2025, 9, 22, 3, 54, 8).get_phase()
        assert '蛾眉月', phase.__str__()
