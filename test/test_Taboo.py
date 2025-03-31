# -*- coding:utf-8 -*-
import unittest

from tyme4py.solar import SolarDay, SolarTime


class TestTaboo(unittest.TestCase):
    def test0(self):
        taboos: [str] = []
        recommends = SolarDay(2024, 6, 26).get_lunar_day().get_recommends()
        for t in recommends:
            taboos.append(t.get_name())
        assert taboos == ['嫁娶', '祭祀', '理发', '作灶', '修饰垣墙', '平治道涂', '整手足甲', '沐浴', '冠笄']

    def test1(self):
        taboos: [str] = []
        avoids = SolarDay(2024, 6, 26).get_lunar_day().get_avoids()
        for t in avoids:
            taboos.append(t.get_name())
        assert taboos, ['破土', '出行', '栽种']

    def test2(self):
        taboos: [str] = []
        recommends = SolarTime(2024, 6, 25, 4, 0, 0).get_lunar_hour().get_recommends()
        for t in recommends:
            taboos.append(t.get_name())
        assert taboos == []

    def test3(self):
        taboos: [str] = []
        avoids = SolarTime(2024, 6, 25, 4, 0, 0).get_lunar_hour().get_avoids()
        for t in avoids:
            taboos.append(t.get_name())
        assert taboos == ['诸事不宜']

    def test4(self):
        taboos: [str] = []
        recommends = SolarTime(2024, 4, 22, 0, 0, 0).get_lunar_hour().get_recommends()
        for t in recommends:
            taboos.append(t.get_name())
        assert taboos == ['嫁娶', '交易', '开市', '安床', '祭祀', '求财']

    def test5(self):
        taboos: [str] = []
        avoids = SolarTime(2024, 4, 22, 0, 0, 0).get_lunar_hour().get_avoids()
        for t in avoids:
            taboos.append(t.get_name())
        assert taboos, ['出行', '移徙', '赴任', '词讼', '祈福', '修造', '求嗣']

    def test6(self):
        taboos: [str] = []
        recommends = SolarDay(2021, 3, 7).get_lunar_day().get_recommends()
        for t in recommends:
            taboos.append(t.get_name())
        assert taboos == ['裁衣', '经络', '伐木', '开柱眼', '拆卸', '修造', '动土', '上梁', '合脊', '合寿木', '入殓', '除服', '成服', '移柩', '破土', '安葬', '启钻', '修坟', '立碑']
