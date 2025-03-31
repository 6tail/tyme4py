# -*- coding:utf-8 -*-
from __future__ import annotations

from tyme4py import LoopTyme
from tyme4py.culture import Luck, Element


class MinorRen(LoopTyme):
    """小六壬"""
    NAMES: [str] = ['大安', '留连', '速喜', '赤口', '小吉', '空亡']
    """名称"""

    def __init__(self, index_or_name: int | str):
        super().__init__(self.NAMES, index_or_name)

    def next(self, n: int) -> MinorRen:
        return MinorRen(self.next_index(n))

    def get_luck(self) -> Luck:
        """
        吉凶
        :return: 吉凶
        """
        return Luck(self.get_index() % 2)

    def get_element(self) -> Element:
        """
        五行
        :return: 五行
        """
        return Element([0, 4, 1, 3, 0, 2][self.get_index()])
