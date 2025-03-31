# -*- coding:utf-8 -*-
import unittest

from tyme4py.sixtycycle import SixtyCycle, EarthBranch, HeavenStem


class TestSixtyCycle(unittest.TestCase):
    def test0(self):
        assert SixtyCycle(13).get_name() == '丁丑'

    def test1(self):
        assert SixtyCycle('丁丑').get_index() == 13

    def test2(self):
        """五行"""
        assert SixtyCycle('辛酉').get_sound().get_name() == '石榴木'
        assert SixtyCycle('癸酉').get_sound().get_name() == '剑锋金'
        assert SixtyCycle('己亥').get_sound().get_name() == '平地木'

    def test3(self):
        """旬"""
        assert SixtyCycle('甲子').get_ten().get_name() == '甲子'
        assert SixtyCycle('乙卯').get_ten().get_name() == '甲寅'
        assert SixtyCycle('癸巳').get_ten().get_name() == '甲申'

    def test4(self):
        """旬空"""
        assert SixtyCycle('甲子').get_extra_earth_branches() == [EarthBranch('戌'), EarthBranch('亥')]
        assert SixtyCycle('乙卯').get_extra_earth_branches() == [EarthBranch('子'), EarthBranch('丑')]
        assert SixtyCycle('癸巳').get_extra_earth_branches() == [EarthBranch('午'), EarthBranch('未')]

    def test5(self):
        """地势(长生十二神)"""
        assert HeavenStem('丙').get_terrain(EarthBranch('寅')).get_name() == '长生'
        assert HeavenStem('辛').get_terrain(EarthBranch('亥')).get_name() == '沐浴'
