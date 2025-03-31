# -*- coding:utf-8 -*-
import unittest

from tyme4py.festival import SolarFestival
from tyme4py.solar import SolarDay


class TestSolarFestival(unittest.TestCase):
    def test2(self):
        f = SolarFestival.from_index(2023, 0)
        assert f
        f1 = f.next(13)
        assert f1
        assert f1.__str__() == '2024年5月1日 五一劳动节'
        f2 = f.next(-3)
        assert f2
        assert f2.__str__() == '2022年8月1日 八一建军节'

    def test3(self):
        f = SolarFestival.from_index(2023, 0)
        assert f
        f1 = f.next(-9)
        assert f1
        assert f1.__str__() == '2022年3月8日 三八妇女节'

    def test4(self):
        f = SolarDay(2010, 1, 1).get_festival()
        assert f
        assert f.__str__() == '2010年1月1日 元旦'

    def test5(self):
        f = SolarDay(2021, 5, 4).get_festival()
        assert f
        assert f.__str__() == '2021年5月4日 五四青年节'

    def test6(self):
        f = SolarDay(1939, 5, 4).get_festival()
        assert f is None
