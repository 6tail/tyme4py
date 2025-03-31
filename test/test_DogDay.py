# -*- coding:utf-8 -*-
import unittest

from tyme4py.solar import SolarDay


class TestDogDay(unittest.TestCase):
    def test(self):
        d = SolarDay(2011, 7, 14).get_dog_day()
        assert d
        assert d.get_name() == '初伏'
        assert d.get_dog().__str__() == '初伏'
        assert d.__str__() == '初伏第1天'

    def test1(self):
        d = SolarDay(2011, 7, 23).get_dog_day()
        assert d
        assert d.get_name() == '初伏'
        assert d.get_dog().__str__() == '初伏'
        assert d.__str__() == '初伏第10天'

    def test2(self):
        d = SolarDay(2011, 7, 24).get_dog_day()
        assert d
        assert d.get_name() == '中伏'
        assert d.get_dog().__str__() == '中伏'
        assert d.__str__() == '中伏第1天'

    def test3(self):
        d = SolarDay(2011, 8, 12).get_dog_day()
        assert d
        assert d.get_name() == '中伏'
        assert d.get_dog().__str__() == '中伏'
        assert d.__str__() == '中伏第20天'

    def test4(self):
        d = SolarDay(2011, 8, 13).get_dog_day()
        assert d
        assert d.get_name() == '末伏'
        assert d.get_dog().__str__() == '末伏'
        assert d.__str__() == '末伏第1天'

    def test5(self):
        d = SolarDay(2011, 8, 22).get_dog_day()
        assert d
        assert d.get_name() == '末伏'
        assert d.get_dog().__str__() == '末伏'
        assert d.__str__() == '末伏第10天'

    def test6(self):
        assert SolarDay(2011, 7, 13).get_dog_day() is None

    def test7(self):
        assert SolarDay(2011, 8, 23).get_dog_day() is None

    def test8(self):
        d = SolarDay(2012, 7, 18).get_dog_day()
        assert d
        assert d.get_name() == '初伏'
        assert d.get_dog().__str__() == '初伏'
        assert d.__str__() == '初伏第1天'

    def test9(self):
        d = SolarDay(2012, 8, 5).get_dog_day()
        assert d
        assert d.get_name() == '中伏'
        assert d.get_dog().__str__() == '中伏'
        assert d.__str__() == '中伏第9天'

    def test10(self):
        d = SolarDay(2012, 8, 8).get_dog_day()
        assert d
        assert d.get_name() == '末伏'
        assert d.get_dog().__str__() == '末伏'
        assert d.__str__() == '末伏第2天'
