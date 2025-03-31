# -*- coding:utf-8 -*-
from __future__ import annotations

from tyme4py import LoopTyme, AbstractCultureDay


class PlumRain(LoopTyme):
    """梅雨"""
    NAMES: [str] = ['入梅', '出梅']
    """名称"""

    def __init__(self, index_or_name: int | str):
        super().__init__(self.NAMES, index_or_name)

    @classmethod
    def from_name(cls, name: str) -> PlumRain:
        return cls(name)

    @classmethod
    def from_index(cls, index: int) -> PlumRain:
        return cls(index)

    def next(self, n: int) -> PlumRain:
        return PlumRain(self.next_index(n))


class PlumRainDay(AbstractCultureDay):
    """梅雨天"""

    def __init__(self, plum_rain: PlumRain, day_index: int):
        super().__init__(plum_rain, day_index)

    def get_plum_rain(self) -> PlumRain:
        """
        梅雨
        :return: 梅雨
        """
        return super().get_culture()

    def __str__(self) -> str:
        return super().__str__() if self.get_plum_rain().get_index() == 0 else self.get_plum_rain().get_name()
