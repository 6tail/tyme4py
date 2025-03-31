# -*- coding:utf-8 -*-
from __future__ import annotations

from tyme4py import LoopTyme
from tyme4py.culture import Luck


class TwelveStar(LoopTyme):
    """黄道黑道十二神"""
    NAMES: [str] = ['青龙', '明堂', '天刑', '朱雀', '金匮', '天德', '白虎', '玉堂', '天牢', '玄武', '司命', '勾陈']
    """名称"""

    def __init__(self, index_or_name: int | str):
        super().__init__(self.NAMES, index_or_name)

    @classmethod
    def from_name(cls, name: str) -> TwelveStar:
        return cls(name)

    @classmethod
    def from_index(cls, index: int) -> TwelveStar:
        return cls(index)

    def next(self, n: int) -> TwelveStar:
        return TwelveStar(self.next_index(n))

    def get_ecliptic(self) -> Ecliptic:
        """
        黄道黑道
        :return: 黄道黑道
        """
        return Ecliptic([0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1][self.get_index()])


class Ecliptic(LoopTyme):
    """黄道黑道就两种，依次为：黄道、黑道。"""
    NAMES: [str] = ["黄道", "黑道"]
    """名称"""

    def __init__(self, index_or_name: int | str):
        super().__init__(self.NAMES, index_or_name)

    @classmethod
    def from_name(cls, name: str) -> Ecliptic:
        return cls(name)

    @classmethod
    def from_index(cls, index: int) -> Ecliptic:
        return cls(index)

    def next(self, n: int) -> Ecliptic:
        return Ecliptic(self.next_index(n))

    def get_luck(self) -> Luck:
        """
        吉凶
        :return: 吉凶
        """
        return Luck(self.get_index())
