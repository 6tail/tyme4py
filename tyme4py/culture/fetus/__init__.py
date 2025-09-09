# -*- coding:utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from tyme4py import LoopTyme, AbstractCulture
from tyme4py.culture import Direction
from tyme4py.enums import Side

if TYPE_CHECKING:
    from tyme4py.lunar import LunarDay, LunarMonth
    from tyme4py.sixtycycle import SixtyCycle, SixtyCycleDay


class FetusEarthBranch(LoopTyme):
    """地支六甲胎神"""
    NAMES: [str] = ['碓', '厕', '炉', '门', '栖', '床']
    """名称"""

    def __init__(self, index_or_name: int | str):
        super().__init__(self.NAMES, index_or_name)

    @classmethod
    def from_name(cls, name: str) -> FetusEarthBranch:
        return cls(name)

    @classmethod
    def from_index(cls, index: int) -> FetusEarthBranch:
        return cls(index)

    def next(self, n: int):
        return FetusEarthBranch(self.next_index(n))


class FetusHeavenStem(LoopTyme):
    """天干六甲胎神"""
    NAMES: [str] = ['门', '碓磨', '厨灶', '仓库', '房床']
    """名称"""

    def __init__(self, index_or_name: int | str):
        super().__init__(self.NAMES, index_or_name)

    @classmethod
    def from_name(cls, name: str) -> FetusHeavenStem:
        return cls(name)

    @classmethod
    def from_index(cls, index: int) -> FetusHeavenStem:
        return cls(index)

    def next(self, n: int) -> FetusHeavenStem:
        return FetusHeavenStem(self.next_index(n))


class FetusMonth(LoopTyme):
    """逐月胎神"""
    NAMES: [str] = ['占房床', '占户窗', '占门堂', '占厨灶', '占房床', '占床仓', '占碓磨', '占厕户', '占门房', '占房床', '占灶炉', '占房床']
    """名称"""

    def __init__(self, index_or_name: int | str):
        super().__init__(self.NAMES, index_or_name)

    @classmethod
    def from_name(cls, name: str) -> FetusMonth:
        return cls(name)

    @classmethod
    def from_index(cls, index: int) -> FetusMonth:
        return cls(index)

    @classmethod
    def from_lunar_month(cls, lunar_month: LunarMonth) -> FetusMonth | None:
        """
        从农历月初始化
        :param lunar_month: 农历月
        :return: 逐月胎神
        """
        return None if lunar_month.is_leap() else cls(lunar_month.get_month() - 1)

    def next(self, n: int) -> FetusMonth:
        return FetusMonth(self.next_index(n))


class FetusDay(AbstractCulture):
    """逐日胎神"""
    _fetus_heaven_stem: FetusHeavenStem
    _fetus_earth_branch: FetusEarthBranch
    _side: Side
    _direction: Direction

    def __init__(self, sixty_cycle: SixtyCycle):
        self._fetus_heaven_stem = FetusHeavenStem(sixty_cycle.get_heaven_stem().get_index() % 5)
        self._fetus_earth_branch = FetusEarthBranch(sixty_cycle.get_earth_branch().get_index() % 6)
        index: int = [3, 3, 8, 8, 8, 8, 8, 1, 1, 1, 1, 1, 1, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, -9, -9, -9, -9, -9, -5, -5, -1, -1, -1, -3, -7, -7, -7, -7, -5, 7, 7, 7, 7, 7, 7, 2, 2, 2, 2, 2, 3, 3, 3, 3][sixty_cycle.get_index()]
        self._side = Side.IN if index < 0 else Side.OUT
        self._direction = Direction(index)

    @classmethod
    def from_lunar_day(cls, lunar_day: LunarDay) -> FetusDay:
        return cls(lunar_day.get_sixty_cycle())

    @classmethod
    def from_sixty_cycle_day(cls, sixty_cycle_day: SixtyCycleDay) -> FetusDay:
        return cls(sixty_cycle_day.get_sixty_cycle())

    def get_name(self) -> str:
        s: str = self._fetus_heaven_stem.get_name() + self._fetus_earth_branch.get_name()
        if '门门' == s:
            s = '占大门'
        elif '碓磨碓' == s:
            s = '占碓磨'
        elif '房床床' == s:
            s = '占房床'
        elif s.startswith('门'):
            s = '占' + s
        s += ' '
        if Side.IN == self._side:
            s += '房内'
        else:
            s += '外'
        direction_name: str = self._direction.get_name()
        if Side.OUT == self._side and '北南西东'.find(direction_name) != -1:
            s += '正'
        s += direction_name
        return s

    def get_side(self) -> Side:
        """
        内外
        :return: 内外
        """
        return self._side

    def get_direction(self) -> Direction:
        """
        方位
        :return: 方位
        """
        return self._direction

    def get_fetus_heaven_stem(self) -> FetusHeavenStem:
        """
        天干六甲胎神
        :return: 天干六甲胎神
        """
        return self._fetus_heaven_stem

    def get_fetus_earth_branch(self) -> FetusEarthBranch:
        """
        地支六甲胎神
        :return: 地支六甲胎神
        """
        return self._fetus_earth_branch
