# -*- coding:utf-8 -*-
from __future__ import annotations

from tyme4py import LoopTyme, AbstractCultureDay


class Dog(LoopTyme):
    """三伏"""
    NAMES: [str] = ['初伏', '中伏', '末伏']
    """名称"""

    def __init__(self, index_or_name: int | str):
        super().__init__(self.NAMES, index_or_name)

    @classmethod
    def from_name(cls, name: str) -> Dog:
        return cls(name)

    @classmethod
    def from_index(cls, index: int) -> Dog:
        return cls(index)

    def next(self, n: int) -> Dog:
        return Dog(self.next_index(n))


class DogDay(AbstractCultureDay):
    """三伏天"""

    def __init__(self, dog: Dog, day_index: int):
        super().__init__(dog, day_index)

    def get_dog(self) -> Dog:
        """
        三伏
        :return: 三伏
        """
        return self.get_culture()
