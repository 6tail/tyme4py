# -*- coding:utf-8 -*-
import unittest

from tyme4py.culture import Element
from tyme4py.sixtycycle import HeavenStem, EarthBranch


class TestElement(unittest.TestCase):
    def test(self):
        assert Element('金').get_restrain().get_name() == Element('木').get_name()

    def test1(self):
        assert Element('火').get_reinforce().get_name() == Element('土').get_name()

    def test2(self):
        assert HeavenStem('丙').get_element().get_name() == '火'

    def test3(self):
        assert EarthBranch('寅').get_element().get_name() == '木'
        assert EarthBranch('寅').get_element().get_reinforce().get_name() == Element('火').get_name()
