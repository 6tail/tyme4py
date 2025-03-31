# -*- coding:utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from tyme4py import LoopTyme
from tyme4py.culture import Land, Animal, Luck, Zone

if TYPE_CHECKING:
    from tyme4py.culture.star.seven import SevenStar


class TwentyEightStar(LoopTyme):
    """二十八宿"""
    NAMES: [str] = ['角', '亢', '氐', '房', '心', '尾', '箕', '斗', '牛', '女', '虚', '危', '室', '壁', '奎', '娄', '胃', '昴', '毕', '觜', '参', '井', '鬼', '柳', '星', '张', '翼', '轸']
    """名称"""

    def __init__(self, index_or_name: int | str):
        super().__init__(self.NAMES, index_or_name)

    @classmethod
    def from_name(cls, name: str) -> TwentyEightStar:
        return cls(name)

    @classmethod
    def from_index(cls, index: int) -> TwentyEightStar:
        return cls(index)

    def next(self, n: int) -> TwentyEightStar:
        return TwentyEightStar(self.next_index(n))

    def get_seven_star(self) -> SevenStar:
        """
        :return: 七曜
        """
        from tyme4py.culture.star.seven import SevenStar
        return SevenStar(self.get_index() % 7 + 4)

    def get_land(self) -> Land:
        """
        :return: 九野
        """
        return Land([4, 4, 4, 2, 2, 2, 7, 7, 7, 0, 0, 0, 0, 5, 5, 5, 6, 6, 6, 1, 1, 1, 8, 8, 8, 3, 3, 3][self.get_index()])

    def get_zone(self) -> Zone:
        """
        :return: 宫
        """
        return Zone(self.get_index() // 7)

    def get_animal(self) -> Animal:
        """
        :return: 动物
        """
        return Animal(self.get_index())

    def get_luck(self) -> Luck:
        """
        :return: 吉凶
        """
        return Luck([0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0][self.get_index()])
