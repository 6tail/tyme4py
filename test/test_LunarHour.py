# -*- coding:utf-8 -*-
import unittest

from tyme4py.lunar import LunarHour


class TestLunarHour(unittest.TestCase):
    def test28(self):
        h: LunarHour = LunarHour(2024, 9, 7, 10, 0, 0)
        assert h.get_minor_ren().get_name() == '留连'
