# -*- coding:utf-8 -*-
import unittest

from tyme4py.rabbyung import RabByungMonth


class TestRabByungMonth(unittest.TestCase):
    def test0(self):
        assert "第十六饶迥铁虎年十二月" == RabByungMonth.from_ym(1950, 12).__str__()
