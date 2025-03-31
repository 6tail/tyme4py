# -*- coding:utf-8 -*-
from __future__ import annotations

from tyme4py import LoopTyme
from tyme4py.culture import Direction, Element


class Dipper(LoopTyme):
    """北斗九星"""
    NAMES: [str] = ['天枢', '天璇', '天玑', '天权', '玉衡', '开阳', '摇光', '洞明', '隐元']
    """名称"""

    def __init__(self, index_or_name: int | str):
        super().__init__(self.NAMES, index_or_name)

    @classmethod
    def from_name(cls, name: str) -> Dipper:
        return cls(name)

    @classmethod
    def from_index(cls, index: int) -> Dipper:
        return cls(index)

    def next(self, n: int) -> Dipper:
        return Dipper(self.next_index(n))


class NineStar(LoopTyme):
    """九星"""
    NAMES: [str] = ['一', '二', '三', '四', '五', '六', '七', '八', '九']
    """名称"""

    def __init__(self, index_or_name: int | str):
        super().__init__(self.NAMES, index_or_name)

    @classmethod
    def from_name(cls, name: str) -> NineStar:
        return cls(name)

    @classmethod
    def from_index(cls, index: int) -> NineStar:
        return cls(index)

    def next(self, n: int) -> NineStar:
        return NineStar(self.next_index(n))

    def get_color(self) -> str:
        """
        颜色
        :return: 颜色
        """
        return ['白', '黑', '碧', '绿', '黄', '白', '赤', '白', '紫'][self.get_index()]

    def get_element(self) -> Element:
        """
        五行
        :return: 五行
        """
        return Element([4, 2, 0, 0, 2, 3, 3, 2, 1][self.get_index()])

    def get_dipper(self) -> Dipper:
        """
        北斗九星
        :return: 北斗九星
        """
        return Dipper(self.get_index())

    def get_direction(self) -> Direction:
        """
        方位
        :return: 方位
        """
        return Direction(self.get_index())

    def __str__(self) -> str:
        return f'{self.get_name()}{self.get_color()}{self.get_element().get_name()}'
