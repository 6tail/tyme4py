# -*- coding:utf-8 -*-
from __future__ import annotations

from tyme4py import LoopTyme


class SixStar(LoopTyme):
    """六曜"""
    NAMES: [str] = ['先胜', '友引', '先负', '佛灭', '大安', '赤口']
    """名称"""

    def __init__(self, index_or_name: int | str):
        super().__init__(self.NAMES, index_or_name)

    @classmethod
    def from_name(cls, name: str) -> SixStar:
        return cls(name)

    @classmethod
    def from_index(cls, index: int) -> SixStar:
        return cls(index)

    def next(self, n: int) -> SixStar:
        return SixStar(self.next_index(n))
