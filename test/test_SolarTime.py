# -*- coding:utf-8 -*-
import unittest

from tyme4py.solar import SolarTime


class TestSolarTime(unittest.TestCase):
    def test0(self):
        time: SolarTime = SolarTime(2023, 1, 1, 13, 5, 20)
        assert time.get_name() == '13:05:20'
        assert time.next(-21).get_name() == '13:04:59'
        assert time.next(41).get_name() == '13:06:01'
