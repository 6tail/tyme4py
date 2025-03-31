# -*- coding:utf-8 -*-
import unittest

from tyme4py.holiday import LegalHoliday


class TestLegalHoliday(unittest.TestCase):
    def test(self):
        d = LegalHoliday.from_ymd(2011, 5, 1)
        assert d is not None
        assert d.__str__() == '2011年5月1日 劳动节(休)'
        d1 = d.next(1)
        assert d1 is not None
        assert d1.__str__() == '2011年5月2日 劳动节(休)'
        d2 = d.next(2)
        assert d2 is not None
        assert d2.__str__() == '2011年6月4日 端午节(休)'
        d3 = d.next(-1)
        assert d3 is not None
        assert d3.__str__() == '2011年4月30日 劳动节(休)'
        d4 = d.next(-2)
        assert d4 is not None
        assert d4.__str__() == '2011年4月5日 清明节(休)'

    def test3(self):
        d = LegalHoliday.from_ymd(2001, 12, 29)
        assert d is not None
        assert d.__str__(), '2001年12月29日 元旦节(班)'
        assert d.next(-1) is None

    def test4(self):
        d = LegalHoliday.from_ymd(2022, 10, 5)
        assert d is not None
        assert d.__str__() == '2022年10月5日 国庆节(休)'
        d1 = d.next(-1)
        assert d1 is not None
        assert d1.__str__() == '2022年10月4日 国庆节(休)'
        d2 = d.next(1)
        assert d2 is not None
        assert d2.__str__() == '2022年10月6日 国庆节(休)'

    def test5(self):
        d = LegalHoliday.from_ymd(2010, 10, 1)
        assert d is not None
        assert d.__str__() == '2010年10月1日 国庆节(休)'
