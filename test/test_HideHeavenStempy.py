# -*- coding:utf-8 -*-


from tyme4py.enums import HideHeavenStemType
from tyme4py.sixtycycle import HideHeavenStemDay
from tyme4py.solar import SolarDay


class TestHideHeavenStem:
    def test0(self):
        d: HideHeavenStemDay = SolarDay(2024, 12, 4).getHideHeavenStemDay()
        assert d.getHideHeavenStem().getType() == HideHeavenStemType.MAIN
        assert d.getHideHeavenStem().get_name() == '壬'
        assert d.getHideHeavenStem().__str__() == '壬'
        assert d.getHideHeavenStem().get_heaven_stem().get_element().get_name() == '水'
        assert d.get_name() == '壬水'
        assert d.getDayIndex() == 15
        assert d.__str__() == '壬水第16天'

    def test1(self):
        d: HideHeavenStemDay = SolarDay(2024, 11, 7).getHideHeavenStemDay()
        assert d.getHideHeavenStem().getType() == HideHeavenStemType.RESIDUAL
        assert d.getHideHeavenStem().get_name() == '戊'
        assert d.getHideHeavenStem().__str__() == '戊'
        assert d.getHideHeavenStem().get_heaven_stem().get_element().get_name() == '土'
        assert d.get_name() == '戊土'
        assert d.getDayIndex() == 0
        assert d.__str__() == '戊土第1天'
