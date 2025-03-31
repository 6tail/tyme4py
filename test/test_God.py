# -*- coding:utf-8 -*-
import unittest

from tyme4py.culture import God
from tyme4py.lunar import LunarDay
from tyme4py.solar import SolarDay


class TestGod(unittest.TestCase):
    def test0(self):
        lunar: LunarDay = SolarDay(2004, 2, 16).get_lunar_day()
        gods: [God] = lunar.get_gods()
        ji: [str] = []
        for god in gods:
            if '吉' == god.get_luck().get_name():
                ji.append(god.get_name())
        xiong: [str] = []
        for god in gods:
            if '凶' == god.get_luck().get_name():
                xiong.append(god.get_name())
        assert ji == ['天恩', '续世', '明堂']
        assert xiong == ['月煞', '月虚', '血支', '天贼', '五虚', '土符', '归忌', '血忌']

    def test1(self):
        lunar: LunarDay = SolarDay(2029, 11, 16).get_lunar_day()
        gods: [God] = lunar.get_gods()
        ji: [str] = []
        for god in gods:
            if '吉' == god.get_luck().get_name():
                ji.append(god.get_name())
        xiong: [str] = []
        for god in gods:
            if '凶' == god.get_luck().get_name():
                xiong.append(god.get_name())
        assert ji == ['天德合', '月空', '天恩', '益后', '金匮']
        assert xiong == ['月煞', '月虚', '血支', '五虚']

    def test2(self):
        lunar: LunarDay = SolarDay(1954, 7, 16).get_lunar_day()
        gods: [God] = lunar.get_gods()
        ji: [str] = []
        for god in gods:
            if '吉' == god.get_luck().get_name():
                ji.append(god.get_name())
        xiong: [str] = []
        for god in gods:
            if '凶' == god.get_luck().get_name():
                xiong.append(god.get_name())
        assert ji == ['民日', '天巫', '福德', '天仓', '不将', '续世', '除神', '鸣吠']
        assert xiong == ['劫煞', '天贼', '五虚', '五离']

    def test3(self):
        lunar: LunarDay = SolarDay(2024, 12, 27).get_lunar_day()
        gods: [God] = lunar.get_gods()
        ji: [str] = []
        for god in gods:
            if '吉' == god.get_luck().get_name():
                ji.append(god.get_name())
        xiong: [str] = []
        for god in gods:
            if '凶' == god.get_luck().get_name():
                xiong.append(god.get_name())
        assert ji == ['天恩', '四相', '阴德', '守日', '吉期', '六合', '普护', '宝光']
        assert xiong == ['三丧', '鬼哭']
