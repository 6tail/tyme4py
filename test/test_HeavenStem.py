# -*- coding:utf-8 -*-
import unittest

from tyme4py.sixtycycle import HeavenStem


class TestHeavenStem(unittest.TestCase):
    def test(self):
        assert HeavenStem(0).get_name() == '甲'

    def test1(self):
        assert HeavenStem('甲').get_index() == 0

    def test2(self):
        assert HeavenStem('甲').get_element().get_reinforce().get_name() == HeavenStem('丙').get_element().get_name()

    def test3(self):
        assert HeavenStem('甲').get_ten_star(HeavenStem('甲')).get_name() == '比肩'
        assert HeavenStem('甲').get_ten_star(HeavenStem('乙')).get_name() == '劫财'
        assert HeavenStem('甲').get_ten_star(HeavenStem('丙')).get_name() == '食神'
        assert HeavenStem('甲').get_ten_star(HeavenStem('丁')).get_name() == '伤官'
        assert HeavenStem('甲').get_ten_star(HeavenStem('戊')).get_name() == '偏财'
        assert HeavenStem('甲').get_ten_star(HeavenStem('己')).get_name() == '正财'
        assert HeavenStem('甲').get_ten_star(HeavenStem('庚')).get_name() == '七杀'
        assert HeavenStem('甲').get_ten_star(HeavenStem('辛')).get_name() == '正官'
        assert HeavenStem('甲').get_ten_star(HeavenStem('壬')).get_name() == '偏印'
        assert HeavenStem('甲').get_ten_star(HeavenStem('癸')).get_name() == '正印'

    def test4(self):
        assert HeavenStem('庚').get_combine().get_name() == '乙'
        assert HeavenStem('乙').get_combine().get_name() == '庚'
        assert HeavenStem('甲').combine(HeavenStem('己')).get_name() == '土'
        assert HeavenStem('己').combine(HeavenStem('甲')).get_name() == '土'
        assert HeavenStem('丁').combine(HeavenStem('壬')).get_name() == '木'
        assert HeavenStem('壬').combine(HeavenStem('丁')).get_name() == '木'
        assert HeavenStem('甲').combine(HeavenStem('乙')) is None
