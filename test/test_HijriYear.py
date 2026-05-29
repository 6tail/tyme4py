# -*- coding:utf-8 -*-
import unittest

from tyme4py.hijri import HijriYear


class TestHijriYear(unittest.TestCase):
    def test(self):
        assert HijriYear.from_year(1).is_leap() is False
        assert HijriYear.from_year(2).is_leap() is True
        assert HijriYear.from_year(0).is_leap() is False
        assert HijriYear.from_year(-1).is_leap() is True
