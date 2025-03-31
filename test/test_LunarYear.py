# -*- coding:utf-8 -*-
import unittest

from tyme4py.lunar import LunarYear


class TestLunarYear(unittest.TestCase):
    def test0(self):
        assert LunarYear(2023).get_name() == '农历癸卯年'

    def test1(self):
        assert LunarYear(2023).next(5).get_name() == '农历戊申年'

    def test2(self):
        assert LunarYear(2023).next(-5).get_name() == '农历戊戌年'

    def test3(self):
        """农历年的干支"""
        assert LunarYear(2020).get_sixty_cycle().get_name() == '庚子'

    def test4(self):
        """农历年的生肖(农历年.干支.地支.生肖)"""
        assert LunarYear(1986).get_sixty_cycle().get_earth_branch().get_zodiac().get_name() == '虎'

    def test5(self):
        assert LunarYear(151).get_leap_month() == 12

    def test6(self):
        assert LunarYear(2357).get_leap_month() == 1

    def test7(self):
        y = LunarYear(2023)
        assert y.get_sixty_cycle().get_name() == '癸卯'
        assert y.get_sixty_cycle().get_earth_branch().get_zodiac().get_name() == '兔'

    def test8(self):
        assert LunarYear(1864).get_twenty().get_sixty().get_name() == '上元'

    def test9(self):
        assert LunarYear(1923).get_twenty().get_sixty().get_name() == '上元'

    def test10(self):
        assert LunarYear(1924).get_twenty().get_sixty().get_name() == '中元'

    def test11(self):
        assert LunarYear(1983).get_twenty().get_sixty().get_name() == '中元'

    def test12(self):
        assert LunarYear(1984).get_twenty().get_sixty().get_name() == '下元'

    def test13(self):
        assert LunarYear(2043).get_twenty().get_sixty().get_name() == '下元'

    def test14(self):
        assert LunarYear(1864).get_twenty().get_name() == '一运'

    def test15(self):
        assert LunarYear(1883).get_twenty().get_name() == '一运'

    def test16(self):
        assert LunarYear(1884).get_twenty().get_name() == '二运'

    def test17(self):
        assert LunarYear(1903).get_twenty().get_name() == '二运'

    def test18(self):
        assert LunarYear(1904).get_twenty().get_name() == '三运'

    def test19(self):
        assert LunarYear(1923).get_twenty().get_name() == '三运'

    def test20(self):
        assert LunarYear(2004).get_twenty().get_name() == '八运'

    def test21(self):
        y = LunarYear(1)
        assert y.get_twenty().get_name() == '六运'
        assert y.get_twenty().get_sixty().get_name() == '中元'

    def test22(self):
        y = LunarYear(1863)
        assert y.get_twenty().get_name() == '九运'
        assert y.get_twenty().get_sixty().get_name() == '下元'
