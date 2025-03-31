# -*- coding:utf-8 -*-
import unittest

from tyme4py.solar import SolarDay


class TestFetus(unittest.TestCase):
    def test(self):
        assert SolarDay(2021, 11, 13).get_lunar_day().get_fetus_day().get_name() == '碓磨厕 外东南'

    def test1(self):
        assert SolarDay(2021, 11, 12).get_lunar_day().get_fetus_day().get_name() == '占门碓 外东南'

    def test2(self):
        assert SolarDay(2011, 11, 12).get_lunar_day().get_fetus_day().get_name() == '厨灶厕 外西南'
