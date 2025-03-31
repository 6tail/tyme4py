# -*- coding:utf-8 -*-
from __future__ import annotations

from tyme4py import LoopTyme, AbstractCultureDay


class Nine(LoopTyme):
    """数九"""
    NAMES: [str] = ['一九', '二九', '三九', '四九', '五九', '六九', '七九', '八九', '九九']
    """名称"""

    def __init__(self, index_or_name: int | str):
        super().__init__(self.NAMES, index_or_name)

    @classmethod
    def from_name(cls, name: str) -> Nine:
        return cls(name)

    @classmethod
    def from_index(cls, index: int) -> Nine:
        return cls(index)

    def next(self, n: int):
        return Nine(self.next_index(n))


class NineDay(AbstractCultureDay):
    """数九天"""

    def __init__(self, nine: Nine, day_index: int):
        super().__init__(nine, day_index)

    def get_nine(self) -> Nine:
        """
        数九
        :return: 数九
        """
        return self.get_culture()

