# -*- coding:utf-8 -*-
import unittest

from tyme4py.sixtycycle import EarthBranch


class TestEarthBranch(unittest.TestCase):
    def test(self):
        assert EarthBranch(0).get_name() == '子'

    def test1(self):
        assert EarthBranch(0).get_index() == 0

    def test2(self):
        assert EarthBranch('子').get_opposite().get_name() == '午'
        assert EarthBranch('戌').get_opposite().get_name() == '辰'

    def test3(self):
        assert EarthBranch('子').get_combine().get_name() == '丑'
        assert EarthBranch('申').get_combine().get_name() == '巳'

    def test4(self):
        assert EarthBranch('巳').get_harm().get_name() == '寅'
        assert EarthBranch('申').get_harm().get_name() == '亥'

    def test5(self):
        # 合化
        assert EarthBranch('卯').combine(EarthBranch('戌')).get_name() == '火'
        assert EarthBranch('戌').combine(EarthBranch('卯')).get_name() == '火'
        # 卯子无法合化
        assert EarthBranch('卯').combine(EarthBranch('子')) is None
