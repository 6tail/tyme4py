# -*- coding:utf-8 -*-
from __future__ import annotations

from tyme4py import LoopTyme


class TenStar(LoopTyme):
    """十神"""
    NAMES: [str] = ['比肩', '劫财', '食神', '伤官', '偏财', '正财', '七杀', '正官', '偏印', '正印']
    """名称"""

    def __init__(self, index_or_name: int | str):
        super().__init__(self.NAMES, index_or_name)

    @classmethod
    def from_name(cls, name: str) -> TenStar:
        return cls(name)

    @classmethod
    def from_index(cls, index: int) -> TenStar:
        return cls(index)

    def next(self, n: int) -> TenStar:
        return TenStar(self.next_index(n))
