# -*- coding:utf-8 -*-
from __future__ import annotations

from tyme4py import LoopTyme
from tyme4py.culture import Week


class SevenStar(LoopTyme):
    """七曜（七政、七纬、七耀）"""
    NAMES: [str] = ['日', '月', '火', '水', '木', '金', '土']
    """名称"""

    def __init__(self, index_or_name: int | str):
        super().__init__(self.NAMES, index_or_name)

    @classmethod
    def from_name(cls, name: str) -> SevenStar:
        return cls(name)

    @classmethod
    def from_index(cls, index: int) -> SevenStar:
        return cls(index)

    def next(self, n: int) -> SevenStar:
        return SevenStar(super().next_index(n))

    def get_week(self) -> Week:
        """
        :return:星期
        """
        return Week(self.get_index())
