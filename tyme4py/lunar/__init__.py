# -*- coding:utf-8 -*-
from __future__ import annotations

import warnings
from math import floor, ceil
from typing import TYPE_CHECKING

from tyme4py import AbstractTyme, LoopTyme
from tyme4py.culture import Twenty, Direction, KitchenGodSteed, Week, Duty, Phase, God, Taboo, PhaseDay
from tyme4py.culture.star.twentyeight import TwentyEightStar
from tyme4py.culture.fetus import FetusMonth, FetusDay
from tyme4py.culture.ren import MinorRen
from tyme4py.culture.star.nine import NineStar
from tyme4py.culture.star.six import SixStar
from tyme4py.culture.star.twelve import TwelveStar
from tyme4py.eightchar import EightChar
from tyme4py.eightchar.provider import EightCharProvider
from tyme4py.eightchar.provider.impl import DefaultEightCharProvider
from tyme4py.festival import LunarFestival
from tyme4py.jd import JulianDay
from tyme4py.util import ShouXingUtil

if TYPE_CHECKING:
    from tyme4py.solar import SolarDay, SolarTime, SolarTerm
    from tyme4py.sixtycycle import SixtyCycle, SixtyCycleDay, SixtyCycleHour, ThreePillars


class LunarYear(AbstractTyme):
    """
    农历年
    依据国家标准《农历的编算和颁行》GB/T 33661-2017，农历年以正月初一开始，至除夕结束。
    """
    _isInit: bool = False
    _LEAP: [[int]] = []
    _year: int

    @staticmethod
    def _init():
        if LunarYear._isInit:
            return
        chars: str = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_@'
        months: [str] = [
            '080b0r0j0j0j0C0j0j0C0j0j0j0C0j0C0j0C0F0j0V0V0V0u0j0j0C0j0j0j0j0V0C0j1v0u0C0V1v0C0b080u110u0C0j0C1v9K1v2z0j1vmZbl1veN3s1v0V0C2S1v0V0C2S2o0C0j1Z1c2S1v0j1c0j2z1v0j1c0j392H0b2_2S0C0V0j1c0j2z0C0C0j0j1c0j0N250j0C0j0b081n080b0C0C0C1c0j0N',
            '0r1v1c1v0V0V0F0V0j0C0j0C0j0V0j0u1O0j0C0V0j0j0j0V0b080u0r0u080b0j0j0C0V0C0V0j0b080V0u080b0j0j0u0j1v0u080b1c0j080b0j0V0j0j0V0C0N1v0j1c0j0j1v2g1v420j1c0j2z1v0j1v5Q9z1v4l0j1vfn1v420j9z4l1v1v2S1c0j1v2S3s1v0V0C2S1v1v2S1c0j1v2S2_0b0j2_2z0j1c0j',
            '0z0j0j0j0C0j0j0C0j0j0j0C0j0C0j0j0j0j0m0j0C0j0j0C0j0j0j0j0b0V0j0j0C0j0j0j0j0V0j0j0j0V0b0V0V0C0V0C0j0j0b080u110u0V0C0j0N0j0b080b080b0j0r0b0r0b0j0j0j0j0C0j0b0r0C0j0b0j0C0C0j0j0j0j0j0j0j0j0j0b110j0b0j0j0j0C0j0C0j0j0j0j0b080b080b0V080b080b0j0j0j0j0j0j0V0j0j0u1v0j0j0j0C0j0j0j0V0C0N1c0j0C0C0j0j0j1n080b0j0V0C0j0C0C2g0j1c0j0j1v2g1v0j0j1v7N0j1c0j3L0j0j1v5Q1Z5Q1v4lfn1v420j1v5Q1Z5Q1v4l1v2z1v',
            '0H140r0N0r140r0u0r0V171c11140C0j0u110j0u0j1v0j0C0j0j0j0b080V0u080b0C1v0j0j0j0C0j0b080V0j0j0b080b0j0j0j0j0b080b0C080j0b080b0j0j0j0j0j0j0b080j0b080C0b080b080b080b0j0j0j0j080b0j0C0j0j0j0b0j0j080C0b0j0j0j0j0j0j0b08080b0j0C0j0j0j0b0j0j0K0b0j0C0j0j0j0b080b080j0C0b0j080b080b0j0j0j0j080b0j0b0r0j0j0j0b0j0C0r0b0j0j0j0j0j0j0j0b080j0b0r0C0j0b0j0j0j0r0b0j0C0j0j0j0u0r0b0C0j080b0j0j0j0j0j0j0j1c0j0b0j0j0j0C0j0j0j0j0j0j0j0b080j1c0u0j0j0j0C0j1c0j0u0j1c0j0j0j0j0j0j0j0j1c0j0u1v0j0j0V0j0j2g0j0j0j0C1v0C1G0j0j0V0C1Z1O0j0V0j0j2g1v0j0j0V0C2g5x1v4l1v421O7N0V0C4l1v2S1c0j1v2S2_',
            '050b080C0j0j0j0C0j0j0C0j0j0j0C0j0C0j0C030j0j0j0j0j0j0j0j0j0C0j0b080u0V080b0j0j0V0j0j0j0j0j0j0j0j0j0V0N0j0C0C0j0j0j0j0j0j0j0j1c0j0u0j1v0j0j0j0j0j0b080b080j0j0j0b080b080b080b080b0j0j0j080b0j0b080j0j0j0j0b080b0j0j0r0b080b0b080j0j0j0j0b080b080j0b080j0b080b080b080b080b0j0j0r0b0j0b080j0j0j0j0b080b0j0j0C080b0b080j0j0j0j0j0j0j0b080u080j0j0b0j0j0j0C0j0b080j0j0j0j0b080b080b080b0C080b080b080b0j0j0j0j0j0j0b0C080j0j0b0j0j0j0C0j0b080j0j0C0b080b080j0b0j0j0C080b0j0j0j0j0j0j0b0j0j080C0b0j080b0j0j0j0j0j0j0j0C0j0j0j0b0j0j0C080b0j0j0j0j0j0j0b080b080b0K0b080b080b0j0j0j0j0j0j0j0C0j0j0u0j0j0V0j080b0j0C0j0j0j0b0j0r0C0b0j0j0j0j0j0j0j0j0j0C0j0b080b080b0j0C0C0j0C0j0j0j0u110u0j0j0j0j0j0j0j0j0C0j0j0u0j1c0j0j0j0j0j0j0j0j0V0C0u0j0C0C0V0C1Z0j0j0j0C0j0j0j1v0u0j1c0j0j0j0C0j0j2g0j1c1v0C1Z0V0j4l0j0V0j0j2g0j1v0j1v2S1c7N1v',
            '0w0j1c0j0V0j0j0V0V0V0j0m0V0j0C1c140j0j0j0C0V0C0j1v0j0N0j0C0j0j0j0V0j0j1v0N0j0j0V0j0j0j0j0j0j080b0j0j0j0j0j0j0j080b0j0C0j0j0j0b0j0j080u080b0j0j0j0j0j0j0b080b080b080C0b0j080b080b0j0j0j0j080b0j0C0j0j0j0b0j0j080u080b0j0j0j0j0j0j0b080b080b080b0r0b0j080b080b0j0j0j0j080b0j0b0r0j0j0b080b0j0j080b0j080b0j080b080b0j0j0j0j0j0b080b0r0C0b080b0j0j0j0j080b0b080b080j0j0j0b080b080b080b0j0j0j0j080b0j0b080j0j0j0j0b080b0j0j0r0b080b0j0j0j0j0j0b080b080j0b0r0b080j0b080b0j0j0j0j080b0j0b080j0j0j0j0b080b0j080b0r0b0j080b080b0j0j0j0j0j0b080b0r0C0b080b0j0j0j0j0j0j0b080j0j0j0b080b080b080b0j0j0j0r0b0j0b080j0j0j0j0b080b0r0b0r0b0j080b080b0j0j0j0j0j0j0b0r0j0j0j0b0j0j0j0j080b0j0b080j0j0j0j0b080b080b0j0r0b0j080b0j0j0j0j0j0j0j0b0r0C0b0j0j0j0j0j0j0j080b0j0C0j0j0j0b0j0C0r0b0j0j0j0j0j0j0b080b080u0r0b0j080b0j0j0j0j0j0j0j0b0r0C0u0j0j0j0C0j080b0j0C0j0j0j0u110b0j0j0j0j0j0j0j0j0j0C0j0b080b0j0j0C0C0j0C0j0j0j0b0j1c0j080b0j0j0j0j0j0j0V0j0j0u0j1c0j0j0j0C0j0j2g0j0j0j0C0j0j0V0j0b080b1c0C0V0j0j2g0j0j0V0j0j1c0j1Z0j0j0C0C0j1v',
            '160j0j0V0j1c0j0C0j0C0j1f0j0V0C0j0j0C0j0j0j1G080b080u0V080b0j0j0V0j1v0j0u0j1c0j0j0j0C0j0j0j0C0C0j1D0b0j080b0j0j0j0j0C0j0b0r0C0j0b0j0C0C0j0j0j0j0j0j0j0j0j0b0r0b0r0j0b0j0j0j0C0j0b0r0j0j0j0b080b080j0b0C0j080b080b0j0j0j0j0j0j0b0C080j0j0b0j0j0j0C0j0b080j0j0j0j0b080b080j0b0C0r0j0b0j0j0j0j0j0j0b0C080j0j0b0j0j0j0C0j0j0j0j0C0j0j0b080b0j0j0C080b0j0j0j0j0j0j0b080b080b080C0b080b080b080b0j0j0j0j0j0b080C0j0j0b080b0j0j0C080b0j0j0j0j0j0j0b080j0b0C080j0j0b0j0j0j0j0j0j0b080j0b080C0b080b080b080b0j0j0j0j080b0j0C0j0j0b080b0j0j0C080b0j0j0j0j0j0j0b080j0b080u080j0j0b0j0j0j0j0j0j0b080C0j0j0b080b0j0j0C0j0j080b0j0j0j0j0j0b080b0C0r0b080b0j0j0j0j0j0j0b080j0b080u080b080b080b0j0j0j0C0j0b080j0j0j0j0b0j0j0j0C0j0j080b0j0j0j0j0j0b080b0C0r0b080b0j0j0j0j0j0j0b080j0b0r0b080b080b080b0j0j0j0r0b0j0b0r0j0j0j0b0j0j0j0r0b0j080b0j0j0j0j0j0j0j0b0r0C0b0j0j0j0j0j0j0j0b080j0C0u080b080b0j0j0j0r0b0j0C0C0j0b0j110b0j080b0j0j0j0j0j0j0u0r0C0b0j0j0j0j0j0j0j0j0j0C0j0j0j0b0j1c0j0C0j0j0j0b0j0814080b080b0j0j0j0j0j0j1c0j0u0j0j0V0j0j0j0j0j0j0j0u110u0j0j0j',
            '020b0r0C0j0j0j0C0j0j0V0j0j0j0j0j0C0j1f0j0C0j0V1G0j0j0j0j0V0C0j0C1v0u0j0j0j0V0j0j0C0j0j0j1v0N0C0V0j0j0j0K0C250b0C0V0j0j0V0j0j2g0C0V0j0j0C0j0j0b081v0N0j0j0V0V0j0j0u0j1c0j080b0j0j0j0j0j0j0V0j0j0u0j0j0V0j0j0j0C0j0b080b080V0b0j080b0j0j0j0j0j0j0j0b0r0C0j0b0j0j0j0C0j080b0j0j0j0j0j0j0u0r0C0u0j0j0j0j0j0j0b080j0C0j0b080b080b0j0C0j080b0j0j0j0j0j0j0b080b110b0j0j0j0j0j0j0j0j0j0b0r0j0j0j0b0j0j0j0r0b0j0b080j0j0j0j0b080b080b080b0r0b0j080b080b0j0j0j0j0j0j0b0r0C0b080b0j0j0j0j080b0j0b080j0j0j0j0b080b080b0j0j0j0r0b0j0j0j0j0j0j0b080b0j080C0b0j080b080b0j0j0j0j080b0j0b0r0C0b080b0j0j0j0j080b0j0j0j0j0j0b080b080b080b0j0j080b0r0b0j0j0j0j0j0j0b0j0j080C0b0j080b080b0j0j0j0j0j0b080C0j0j0b080b0j0j0C0j0b080j0j0j0j0b080b080b080b0C0C080b0j0j0j0j0j0j0b0C0C080b080b080b0j0j0j0j0j0j0b0C080j0j0b0j0j0j0C0j0b080j0b080j0j0b080b080b080b0C0r0b0j0j0j0j0j0j0b080b0r0b0r0b0j080b080b0j0j0j0j0j0j0b0r0C0j0b0j0j0j0j0j0j0b080j0C0j0b080j0b0j0j0K0b0j0C0j0j0j0b080b0j0K0b0j080b0j0j0j0j0j0j0V0j0j0b0j0j0j0C0j0j0j0j',
            '0l0C0K0N0r0N0j0r1G0V0m0j0V1c0C0j0j0j0j1O0N110u0j0j0j0C0j0j0V0C0j0u110u0j0j0j0C0j0j0j0C0C0j250j1c2S1v1v0j5x2g0j1c0j0j1c2z0j1c0j0j1c0j0N1v0V0C1v0C0b0C0V0j0j0C0j0C1v0u0j0C0C0j0j0j0C0j0j0j0u110u0j0j0j0C0j0C0C0C0b080b0j0C0j080b0j0C0j0j0j0u110u0j0j0j0C0j0j0j0C0j0j0j0u0C0r0u0j0j0j0j0j0j0b0r0b0V080b080b0j0C0j0j0j0V0j0j0b0j0j0j0C0j0j0j0j0j0j0j0b080j0b0C0r0j0b0j0j0j0C0j0b0r0b0r0j0b080b080b0j0C0j0j0j0j0j0j0j0j0b0j0C0r0b0j0j0j0j0j0j0b080b080j0b0r0b0r0j0b0j0j0j0j080b0j0b0r0j0j0j0b080b080b0j0j0j0j080b0j0j0j0j0j0j0b0j0j0j0r0b0j0j0j0j0j0j0b080b080b080b0r0C0b080b0j0j0j0j0j0b080b0r0C0b080b080b080b0j0j0j0j080b0j0C0j0j0j0b0j0j0C080b0j0j0j0j0j0j0b080j0b0C080j0j0b0j0j0j0j0j0j0b0r0b080j0j0b080b080b0j0j0j0j0j0j0b080j0j0j0j0b0j0j0j0r0b0j0b080j0j0j0j0j0b080b080b0C0r0b0j0j0j0j0j0j0b080b080j0C0b0j080b080b0j0j0j0j0j0j',
            '0a0j0j0j0j0C0j0j0C0j0C0C0j0j0j0j0j0j0j0m0C0j0j0j0j0u080j0j0j1n0j0j0j0j0C0j0j0j0V0j0j0j1c0u0j0C0V0j0j0V0j0j1v0N0C0V2o1v1O2S2o141v0j1v4l0j1c0j1v2S2o0C0u1v0j0C0C2S1v0j1c0j0j1v0N251c0j1v0b1c1v1n1v0j0j0V0j0j1v0N1v0C0V0j0j1v0b0C0j0j0V1c0j0u0j1c0j0j0j0j0j0j0j0j1c0j0u0j0j0V0j0j0j0j0j0j0b080u110u0j0j0j0j0j0j1c0j0b0j080b0j0C0j0j0j0V0j0j0u0C0V0j0j0j0C0j0b080j1c0j0b0j0j0j0C0j0C0j0j0j0b080b080b0j0C0j080b0j0j0j0j0j0j0j0b0C0r0u0j0j0j0j0j0j0b080j0b0r0C0j0b0j0j0j0r0b0j0b0r0j0j0j0b080b080b0j0r0b0j080b0j0j0j0j0j0j0b0j0r0C0b0j0j0j0j0j0j0b080j0j0C0j0j0b080b0j0j0j0j0j0j0j0j0j0j0b080b080b080b0C0j0j080b0j0j0j0j0j0j0b0j0j0C080b0j0j0j0j0j0j0j0j0b0C080j0j0b0j0j0j0j0j',
            '0n0Q0j1c14010q0V1c171k0u0r140V0j0j1c0C0N1O0j0V0j0j0j1c0j0u110u0C0j0C0V0C0j0j0b671v0j1v5Q1O2S2o2S1v4l1v0j1v2S2o0C1Z0j0C0C1O141v0j1c0j2z1O0j0V0j0j1v0b2H390j1c0j0V0C2z0j1c0j1v2g0C0V0j1O0b0j0j0V0C1c0j0u0j1c0j0j0j0j0j0j0j0j1c0N0j0j0V0j0j0C0j0j0b081v0u0j0j0j0C0j1c0N0j0j0C0j0j0j0C0j0j0j0u0C0r0u0j0j0j0C0j0b080j1c0j0b0j0C0C0j0C0C0j0b080b080u0C0j080b0j0C0j0j0j0u110u0j0j0j0j0j0j0j0j0C0C0j0b0j0j0j0C0j0C0C0j0b080b080b0j0C0j080b0j0C0j0j0j0b0j110b0j0j0j0j0j',
            '0B0j0V0j0j0C0j0j0j0C0j0C0j0j0C0j0m0j0j0j0j0C0j0C0j0j0u0j1c0j0j0C0C0j0j0j0j0j0j0j0j0u110N0j0j0V0C0V0j0b081n080b0CrU1O5e2SbX2_1Z0V2o141v0j0C0C0j2z1v0j1c0j7N1O420j1c0j1v2S1c0j1v2S2_0b0j0V0j0j1v0N1v0j0j1c0j1v140j0V0j0j0C0C0b080u1v0C0V0u110u0j0j0j0C0j0j0j0C0C0N0C0V0j0j0C0j0j0b080u110u0C0j0C0u0r0C0u080b0j0j0C0j0j0j'
        ]
        for m in months:
            n: int = 0
            size: int = int(m.__len__() / 2)
            l: [int] = []
            for y in range(0, size):
                z: int = y * 2
                t: int = 0
                c: int = 1
                for x in range(1, -1, -1):
                    t += c * chars.index(m[z + x])
                    c *= 64
                n += t
                l.append(n)
            LunarYear._LEAP.append(l)
        LunarYear._isInit = True

    def __init__(self, year: int):
        LunarYear._init()
        if year < -1 or year > 9999:
            raise ValueError(f'illegal lunar year: {year}')
        self._year = year

    @classmethod
    def from_year(cls, year: int) -> LunarYear:
        return cls(year)

    def get_year(self) -> int:
        """
        年
        :return: 返回为农历年数字，范围为-1到9999。
        """
        return self._year

    def get_day_count(self) -> int:
        """
        当年的总天数
        :return: 返回为数字，从正月初一到除夕的总天数。
        """
        n: int = 0
        months: [LunarMonth] = self.get_months()
        for i in range(0, months.__len__()):
            n += months[i].get_day_count()
        return n

    def get_month_count(self) -> int:
        """
        当年的总月数
        :return: 返回为数字，有闰月为13，无闰月为12
        """
        return 12 if self.get_leap_month() < 1 else 13

    def get_name(self) -> str:
        """
        :return: 农历{六十甲子}年
        """
        return f'农历{self.get_sixty_cycle().get_name()}年'

    def next(self, n: int) -> LunarYear:
        return LunarYear(self._year + n)

    def get_leap_month(self) -> int:
        """
        当年的闰月月份
        :return: 返回为数字，代表当年的闰月月份，例如：5代表闰五月，0代表当年没有闰月。
        """
        if self._year == -1:
            return 11
        for i in range(0, self._LEAP.__len__()):
            if self._year in self._LEAP[i]:
                return i + 1
        return 0

    def get_sixty_cycle(self) -> SixtyCycle:
        """
        当年的干支
        :return: 干支 SixtyCycle
        """
        from tyme4py.sixtycycle import SixtyCycle
        return SixtyCycle(self._year - 4)

    def get_twenty(self) -> Twenty:
        """
        :return: 返回为运 Twenty。
        """
        return Twenty(floor((self._year - 1864) / 20))

    def get_nine_star(self) -> NineStar:
        """
        :return: 返回为九星 NineStar。
        """
        return NineStar(63 + self.get_twenty().get_sixty().get_index() * 3 - self.get_sixty_cycle().get_index())

    def get_jupiter_direction(self) -> Direction:
        """
        太岁方位
        :return: 返回为方位 Direction。
        """
        return Direction([0, 7, 7, 2, 3, 3, 8, 1, 1, 6, 0, 0][self.get_sixty_cycle().get_earth_branch().get_index()])

    def get_first_month(self) -> LunarMonth:
        """
        首月（农历月，即一月，俗称正月）
        :return: 农历月
        """
        return LunarMonth.from_ym(self._year, 1)

    def get_months(self) -> list[LunarMonth]:
        """
        农历月列表
        :return: 农历月 LunarMonth 的列表，从正月到十二月，包含闰月。
        """
        l: [LunarMonth] = []
        m: LunarMonth = self.get_first_month()
        while m.get_year() == self._year:
            l.append(m)
            m = m.next(1)
        return l

    def get_kitchen_god_steed(self) -> KitchenGodSteed:
        """
        灶马头
        :return: 灶马头
        """
        return KitchenGodSteed.from_lunar_year(self._year)


class LunarSeason(LoopTyme):
    """
    农历季节
    从正月开始，依次为：孟春、仲春、季春、孟夏、仲夏、季夏、孟秋、仲秋、季秋、孟冬、仲冬、季冬。
    """
    NAMES: [str] = ['孟春', '仲春', '季春', '孟夏', '仲夏', '季夏', '孟秋', '仲秋', '季秋', '孟冬', '仲冬', '季冬']
    """名称"""

    def __init__(self, index_or_name: int | str):
        super().__init__(self.NAMES, index_or_name)

    @classmethod
    def from_name(cls, name: str) -> LunarSeason:
        return cls(name)

    @classmethod
    def from_index(cls, index: int) -> LunarSeason:
        return cls(index)

    def next(self, n: int) -> LunarSeason:
        return LunarSeason(self.next_index(n))


class LunarMonth(AbstractTyme):
    """
    农历月
    农历月以初一开始，大月30天，小月29天。
    """
    _cache: {str: [int]} = {}
    NAMES: [str] = ['正月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']
    _year: LunarYear
    """农历年"""
    _month: int
    """月"""
    _leap: bool
    """是否闰月"""
    _day_count: int
    """天数"""
    _index_in_year: int
    """位于当年的索引，0-12"""
    _first_julian_day: JulianDay
    """初一的儒略日"""

    def __init__(self, year: int, month: int, cache: [int] or None = None):
        """
        :param year: 农历年
        :param month: 农历月，闰月为负
        :param cache: 缓存[农历年(int)，农历月(int,闰月为负)，天数(int)，位于当年的索引(int)，初一的儒略日(double)]
        """
        from tyme4py.jd import JulianDay
        # 从缓存初始化
        if cache:
            m: int = cache[1]
            self._year = LunarYear(cache[0])
            self._month = abs(m)
            self._leap = m < 0
            self._day_count = cache[2]
            self._index_in_year = cache[3]
            self._first_julian_day = JulianDay(cache[4])
        else:
            current_year: LunarYear = LunarYear(year)
            current_leap_month: int = current_year.get_leap_month()
            if month == 0 or month > 12 or month < -12:
                raise ValueError(f'illegal lunar month: {month}')
            leap: bool = month < 0
            m: int = abs(month)
            if leap and m != current_leap_month:
                raise ValueError(f'illegal leap month {m} in lunar year {year}')

            from tyme4py.solar import SolarTerm
            # 冬至
            dong_zhi_jd: float = SolarTerm(year, 0).get_cursory_julian_day()
            # 冬至前的初一，今年首朔的日月黄经差
            w: int = ShouXingUtil.calc_shuo(dong_zhi_jd)
            if w > dong_zhi_jd:
                w -= 29.53

            # 正常情况正月初一为第3个朔日，但有些特殊的
            offset: int = 2
            if 8 < year < 24:
                offset = 1
            elif LunarYear(year - 1).get_leap_month() > 10 and year != 239 and year != 240:
                offset = 3

            # 位于当年的索引
            index: int = m - 1
            if leap or (0 < current_leap_month < m):
                index += 1
            self._index_in_year = index
            # 本月初一
            w += 29.5306 * (offset + index)
            first_day: int = ShouXingUtil.calc_shuo(w)
            self._first_julian_day = JulianDay(JulianDay.J2000 + first_day)

            # 本月天数 = 下月初一 - 本月初一
            self._day_count = ~~(ShouXingUtil.calc_shuo(w + 29.5306) - first_day)
            self._year = current_year
            self._month = m
            self._leap = leap

    @classmethod
    def from_ym(cls, year: int, month: int) -> LunarMonth:
        """
        从农历年、月初始化
        :param year: 农历年，支持从-1到9999年；
        :param month:  农历月，支持1到12，如果为闰月的，使用负数，即-3代表闰三月。
        :return: LunarMonth
        """
        m: LunarMonth
        key: str = f'{year:04}{month:02}'
        try:
            cache: [int] = LunarMonth._cache[key]
            m = cls(0, 0, cache)
        except KeyError:
            m = cls(year, month)
            LunarMonth._cache[key] = [m.get_year(), m.get_month_with_leap(), m.get_day_count(), m.get_index_in_year(), m.get_first_julian_day().get_day()]
        return m

    def get_lunar_year(self) -> LunarYear:
        """
        农历年
        :return: 农历年
        """
        return self._year

    def get_year(self) -> int:
        """
        农历年
        :return: 农历年
        """
        return self._year.get_year()

    def get_month(self) -> int:
        """
        月份
        :return: 返回为月份数字，范围为1到12，如闰七月也返回7。
        """
        return self._month

    def get_month_with_leap(self) -> int:
        """
        月(支持闰月)
        :return: 返回为月份数字，范围为1到12，闰月为负数，如闰7月返回-7。
        """
        return -self._month if self._leap else self._month

    def get_day_count(self) -> int:
        """
        当月的总天数
        :return:返回为数字，从初一开始的总天数，大月有30天，小月有29天。
        """
        return self._day_count

    def get_index_in_year(self) -> int:
        """
        位于当年的月索引
        :return: 返回为数字，范围0到12，正月为0，依次类推，例如五月索引值为4，闰五月索引值为5。
        """
        return self._index_in_year

    def get_season(self) -> LunarSeason:
        """
        :return: 农历季节
        """
        return LunarSeason(self._month - 1)

    def get_first_julian_day(self) -> JulianDay:
        """
        初一的儒略日
        :return: 儒略日
        """
        return self._first_julian_day

    def is_leap(self) -> bool:
        """
        是否闰月
        :return: 返回为布尔值，闰月返回true，非闰月返回false。
        """
        return self._leap

    def get_week_count(self, start: int) -> int:
        """
        当月有几周
        :param start: 参数为起始星期，1234560分别代表星期一至星期天
        :return: 返回为数字。
        """
        return ceil((self.index_of(self._first_julian_day.get_week().get_index() - start, 7) + self.get_day_count()) / 7)

    def get_name(self) -> str:
        """
        依据国家标准《农历的编算和颁行》GB/T 33661-2017中农历月的命名方法。
        :return: 名称
        """
        return ('闰' if self._leap else '') + self.NAMES[self._month - 1]

    def __str__(self) -> str:
        return self._year.__str__() + self.get_name()

    def next(self, n: int) -> LunarMonth:
        if n == 0:
            return LunarMonth.from_ym(self.get_year(), self.get_month_with_leap())

        m: int = self._index_in_year + 1 + n
        y: LunarYear = self._year
        if n > 0:
            month_count: int = y.get_month_count()
            while m > month_count:
                m -= month_count
                y = y.next(1)
                month_count = y.get_month_count()
        else:
            while m <= 0:
                y = y.next(-1)
                m += y.get_month_count()

        leap: bool = False
        leap_month: int = y.get_leap_month()
        if leap_month > 0:
            if m == leap_month + 1:
                leap = True
            if m > leap_month:
                m -= 1
        return LunarMonth.from_ym(y.get_year(), -m if leap else m)

    def get_days(self) -> list[LunarDay]:
        """
        本月的农历日列表
        :return: 农历日 LunarDay 的列表，从初一开始。
        """
        y: int = self.get_year()
        m: int = self.get_month_with_leap()
        l: [LunarDay] = []
        for i in range(1, self.get_day_count() + 1):
            l.append(LunarDay(y, m, i))
        return l

    def get_weeks(self, start: int) -> list[LunarWeek]:
        """
        本月的农历周列表
        :param start: 参数为起始星期，1234560分别代表星期一至星期天
        :return: 农历周 LunarWeek 的列表。
        """
        y: int = self.get_year()
        m: int = self.get_month_with_leap()
        l: [LunarWeek] = []
        for i in range(0, self.get_week_count(start)):
            l.append(LunarWeek(y, m, i, start))
        return l

    def get_sixty_cycle(self) -> SixtyCycle:
        """
        当月的干支
        :return: 干支 SixtyCycle。
        """
        from tyme4py.sixtycycle import SixtyCycle, HeavenStem, EarthBranch
        return SixtyCycle(HeavenStem(self._year.get_sixty_cycle().get_heaven_stem().get_index() * 2 + self._month + 1).get_name() + EarthBranch(self._month + 1).get_name())

    def get_nine_star(self) -> NineStar:
        """
        :return: 九星 NineStar。
        """
        index = self.get_sixty_cycle().get_earth_branch().get_index()
        if index < 2:
            index += 3
        return NineStar(27 - self._year.get_sixty_cycle().get_earth_branch().get_index() % 3 * 3 - index)

    def get_jupiter_direction(self) -> Direction:
        """
        太岁方位
        :return: 方位 Direction。
        """
        from tyme4py.sixtycycle import SixtyCycle
        sixty_cycle: SixtyCycle = self.get_sixty_cycle()
        n: int = [7, -1, 1, 3][sixty_cycle.get_earth_branch().next(-2).get_index() % 4]
        return Direction(n) if n != -1 else sixty_cycle.get_heaven_stem().get_direction()

    def get_fetus(self) -> FetusMonth | None:
        """
        :return: 返回为逐月胎神 FetusMonth。闰月无胎神。
        """
        return FetusMonth.from_lunar_month(self)

    def get_minor_ren(self) -> MinorRen:
        """
        :return: 小六壬
        """
        return MinorRen((self._month - 1) % 6)


class LunarWeek(AbstractTyme):
    """
    农历周
    农历一个月最多有6个周，分别为：第一周、第二周、第三周、第四周、第五周、第六周。
    """
    NAMES: [str] = ['第一周', '第二周', '第三周', '第四周', '第五周', '第六周']
    """名称"""
    _month: LunarMonth
    """月"""
    _index: int
    """索引，0-5"""
    _start: Week
    """起始星期"""

    def __init__(self, year: int, month: int, index: int, start: int):
        """
        :param year: 年
        :param month: 月
        :param index: 周索引，0-5
        :param start: 起始星期  (1234560分别代表星期一至星期日)
        """
        if index < 0 or index > 5:
            raise ValueError(f'illegal lunar week index: {index}')
        if start < 0 or start > 6:
            raise ValueError(f'illegal lunar week start: {start}')
        m: LunarMonth = LunarMonth.from_ym(year, month)
        if index >= m.get_week_count(start):
            raise ValueError(f'illegal lunar week index: {index} in month: {m}')

        self._month = m
        self._index = index
        self._start = Week(start)

    @classmethod
    def from_ym(cls, year: int, month: int, index: int, start: int) -> LunarWeek:
        return cls(year, month, index, start)

    def get_lunar_month(self) -> LunarMonth:
        """
        :return:农历月
        """
        return self._month

    def get_year(self) -> int:
        """
        :return: 农历年数字
        """
        return self._month.get_year()

    def get_month(self) -> int:
        """
        :return: 农历月数字
        """
        return self._month.get_month_with_leap()

    def get_index(self) -> int:
        """
        :return:  索引，0-5
        """
        return self._index

    def get_start(self) -> Week:
        """
        起始星期
        :return:  星期
        """
        return self._start

    def get_name(self) -> str:
        return self.NAMES[self._index]

    def __str__(self) -> str:
        return f'{self._month.__str__()}{self.get_name()}'

    def next(self, n: int) -> LunarWeek:
        start_index: int = self._start.get_index()
        if n == 0:
            return LunarWeek(self.get_year(), self.get_month(), self._index, start_index)

        d: int = self._index + n
        m: LunarMonth = self._month
        if n > 0:
            week_count: int = m.get_week_count(start_index)
            while d >= week_count:
                d -= week_count
                m = m.next(1)
                if not LunarDay(m.get_year(), m.get_month_with_leap(), 1).get_week() == self._start:
                    d += 1
                week_count = m.get_week_count(start_index)
        else:
            while d < 0:
                if not LunarDay(m.get_year(), m.get_month_with_leap(), 1).get_week() == self._start:
                    d -= 1
                m = m.next(-1)
                d += m.get_week_count(start_index)
        return LunarWeek(m.get_year(), m.get_month_with_leap(), d, start_index)

    def get_first_day(self) -> LunarDay:
        """
        本周第一天的农历日
        :return: 农历日 LunarDay。
        """
        first_day: LunarDay = LunarDay(self.get_year(), self.get_month(), 1)
        return first_day.next(self._index * 7 - self.index_of(first_day.get_week().get_index() - self._start.get_index(), 7))

    def get_days(self) -> list[LunarDay]:
        """
        本周农历日列表
        :return: 农历日 LunarDay的列表。
        """
        l: [LunarDay] = []
        d: LunarDay = self.get_first_day()
        l.append(d)
        for i in range(1, 7):
            l.append(d.next(i))
        return l

    def __eq__(self, other: LunarWeek) -> bool:
        return other and other.get_first_day() == self.get_first_day()


class LunarDay(AbstractTyme):
    """农历日"""
    NAMES: [str] = ['初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十', '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十', '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十']
    """名称"""
    _month: LunarMonth
    """农历月"""
    _day: int
    """日"""
    _solar_day: SolarDay = None
    """公历日（第一次使用时才会初始化）"""
    _sixty_cycle_day: SixtyCycleDay = None
    """干支日（第一次使用时才会初始化）"""

    def __init__(self, year: int, month: int, day: int):
        """
        :param year: 农历年
        :param month: 农历月，闰月为负
        :param day: 农历日
        """
        m: LunarMonth = LunarMonth.from_ym(year, month)
        if day < 1 or day > m.get_day_count():
            raise ValueError(f'illegal day {day} in {m}')
        self._month = m
        self._day = day

    @classmethod
    def from_ymd(cls, year: int, month: int, day: int) -> LunarDay:
        return cls(year, month, day)

    def get_lunar_month(self) -> LunarMonth:
        """
        :return: 农历月
        """
        return self._month

    def get_year(self) -> int:
        """
        :return: 农历年 number
        """
        return self._month.get_year()

    def get_month(self) -> int:
        """
        :return: 农历月 number
        """
        return self._month.get_month_with_leap()

    def get_day(self) -> int:
        """
        日
        :return: 数字，范围1到30。
        """
        return self._day

    def get_name(self) -> str:
        """
        :return:农历日名，'初一'
        """
        return self.NAMES[self._day - 1]

    def __str__(self) -> str:
        return f'{self._month.__str__()}{self.get_name()}'

    def next(self, n: int) -> LunarDay:
        return self.get_solar_day().next(n).get_lunar_day()

    def is_before(self, target: LunarDay) -> bool:
        """
        是否在指定农历日之前
        :param target:农历日 LunarDay
        :return: true/false
        """
        a_year: int = self.get_year()
        b_year: int = target.get_year()
        if a_year != b_year:
            return a_year < b_year
        a_month: int = self.get_month()
        b_month: int = target.get_month()
        if a_month != b_month:
            return abs(a_month) < abs(b_month)
        return self._day < target.get_day()

    def is_after(self, target: LunarDay) -> bool:
        """
        是否在指定农历日之后
        :param target:农历日 LunarDay
        :return:
        """
        a_year: int = self.get_year()
        b_year: int = target.get_year()
        if a_year != b_year:
            return a_year > b_year
        a_month: int = self.get_month()
        b_month: int = target.get_month()
        if a_month != b_month:
            return abs(a_month) >= abs(b_month)
        return self._day > target.get_day()

    def get_week(self) -> Week:
        """
        :return: 星期
        """
        return self.get_solar_day().get_week()

    def get_year_sixty_cycle(self) -> SixtyCycle:
        """
        当天的年干支 非当天所属的农历年干支，以立春换年。
        :return: 干支 SixtyCycle
        """
        warnings.warn('get_year_sixty_cycle() is deprecated, please use SixtyCycleDay.get_year() instead.', DeprecationWarning)
        return self.get_sixty_cycle_day().get_year()

    def get_month_sixty_cycle(self) -> SixtyCycle:
        """
        当天的月干支 非当天所属的农历月干支，以节令换月。
        :return: 干支 SixtyCycle
        """
        warnings.warn('get_month_sixty_cycle() is deprecated, please use SixtyCycleDay.get_month() instead.', DeprecationWarning)
        return self.get_sixty_cycle_day().get_month()

    def get_sixty_cycle(self) -> SixtyCycle:
        """
        当天的干支
        :return: 干支
        """
        from tyme4py.sixtycycle import SixtyCycle, HeavenStem, EarthBranch
        offset: int = int(self._month.get_first_julian_day().next(self._day - 12).get_day())
        return SixtyCycle(HeavenStem(offset).get_name() + EarthBranch(offset).get_name())

    def get_duty(self) -> Duty:
        """
        建除十二值神
        :return: 建除十二值神 Duty
        """
        return self.get_sixty_cycle_day().get_duty()

    def get_twelve_star(self) -> TwelveStar:
        """
        黄道黑道十二神
        :return: 黄道黑道十二神 TwelveStar
        """
        return self.get_sixty_cycle_day().get_twelve_star()

    def get_nine_star(self) -> NineStar:
        """
        :return: 九星 NineStar。
        """
        from tyme4py.solar import SolarTerm
        d: SolarDay = self.get_solar_day()
        dong_zhi: SolarTerm = SolarTerm(d.get_year(), 0)
        dong_zhi_solar: SolarDay = dong_zhi.get_solar_day()
        xia_zhi_solar: SolarDay = dong_zhi.next(12).get_solar_day()
        dong_zhi_solar2: SolarDay = dong_zhi.next(24).get_solar_day()
        dong_zhi_index: int = dong_zhi_solar.get_lunar_day().get_sixty_cycle().get_index()
        xia_zhi_index: int = xia_zhi_solar.get_lunar_day().get_sixty_cycle().get_index()
        dong_zhi_index2: int = dong_zhi_solar2.get_lunar_day().get_sixty_cycle().get_index()
        solar_shun_bai: SolarDay = dong_zhi_solar.next(60 - dong_zhi_index if dong_zhi_index > 29 else -dong_zhi_index)
        solar_shun_bai2: SolarDay = dong_zhi_solar2.next(60 - dong_zhi_index2 if dong_zhi_index2 > 29 else -dong_zhi_index2)
        solar_ni_zi: SolarDay = xia_zhi_solar.next(60 - xia_zhi_index if xia_zhi_index > 29 else -xia_zhi_index)
        offset: int = 0
        if not d.is_before(solar_shun_bai) and d.is_before(solar_ni_zi):
            offset = d.subtract(solar_shun_bai)
        elif not d.is_before(solar_ni_zi) and d.is_before(solar_shun_bai2):
            offset = 8 - d.subtract(solar_ni_zi)
        elif not d.is_before(solar_shun_bai2):
            offset = d.subtract(solar_shun_bai2)
        elif d.is_before(solar_shun_bai):
            offset = 8 + solar_shun_bai.subtract(d)
        return NineStar(offset)

    def get_jupiter_direction(self) -> Direction:
        """
        太岁方位
        :return: 方位 Direction。
        """
        index: int = self.get_sixty_cycle().get_index()
        from tyme4py.culture import Element
        return Element(index // 12).get_direction() if index % 12 < 6 else self._month.get_lunar_year().get_jupiter_direction()

    def get_fetus_day(self) -> FetusDay:
        """
        :return:逐日胎神 FetusDay。
        """
        return FetusDay.from_lunar_day(self)

    def get_phase_day(self) -> PhaseDay:
        """
        月相第几天
        :return: 月相第几天
        """
        today = self.get_solar_day()
        m = self._month.next(1)
        p = Phase.from_index(m.get_year(), m.get_month_with_leap(), 0)
        d = p.get_solar_day()
        while d.is_after(today):
            p = p.next(-1)
            d = p.get_solar_day()
        return PhaseDay(p, today.subtract(d))

    def get_phase(self) -> Phase:
        """
        月相
        :return: 月相 Phase。
        """
        return self.get_phase_day().get_phase()

    def get_solar_day(self) -> SolarDay:
        """
        公历日
        :return: 公历日 SolarDay。
        """
        if self._solar_day is None:
            self._solar_day = self._month.get_first_julian_day().next(self._day - 1).get_solar_day()
        return self._solar_day

    def get_sixty_cycle_day(self) -> SixtyCycleDay:
        """
        干支日
        :return: 干支日
        """
        if self._sixty_cycle_day is None:
            self._sixty_cycle_day = self.get_solar_day().get_sixty_cycle_day()
        return self._sixty_cycle_day

    def get_twenty_eight_star(self) -> TwentyEightStar:
        """
        :return: 二十八宿 TwentyEightStar。
        """
        return TwentyEightStar([10, 18, 26, 6, 14, 22, 2][self.get_solar_day().get_week().get_index()]).next(-7 * self.get_sixty_cycle().get_earth_branch().get_index())

    def get_festival(self) -> LunarFestival | None:
        """
        农历传统节日，如果当天不是农历传统节日，返回None
        :return:农历传统节日 LunarFestival
        """
        return LunarFestival.from_ymd(self.get_year(), self.get_month(), self._day)

    def get_six_star(self) -> SixStar:
        """
        :return: 六曜
        """
        return SixStar((self._month.get_month() + self._day - 2) % 6)

    def get_gods(self) -> list[God]:
        """
        神煞列表(吉神宜趋，凶神宜忌)
        :return: 神煞列表
        """
        return self.get_sixty_cycle_day().get_gods()

    def get_recommends(self) -> list[Taboo]:
        """
        今日 宜
        :return: 宜忌列表
        """
        return self.get_sixty_cycle_day().get_recommends()

    def get_avoids(self) -> list[Taboo]:
        """
        今日 忌
        :return: 宜忌列表
        """
        return self.get_sixty_cycle_day().get_avoids()

    def get_hours(self) -> list[LunarHour]:
        """
        当天的时辰列表
        :return: 由于23:00-23:59、00:00-00:59均为子时，而农历日是从00:00-23:59为一天，所以获取当天的时辰列表，实际会返回13个。
        """
        l: [LunarHour] = []
        y: int = self.get_year()
        m: int = self.get_month()
        l.append(LunarHour(y, m, self._day, 0, 0, 0))
        for i in range(0, 24, 2):
            l.append(LunarHour(y, m, self._day, i + 1, 0, 0))
        return l

    def get_minor_ren(self) -> MinorRen:
        """
        小六壬
        :return: 小六壬
        """
        return self.get_lunar_month().get_minor_ren().next(self._day - 1)

    def get_three_pillars(self) -> ThreePillars:
        """
        三柱
        @return: 三柱
        """
        return self.get_sixty_cycle_day().get_three_pillars()


class LunarHour(AbstractTyme):
    """
    农历时辰
    """
    provider: EightCharProvider = DefaultEightCharProvider()
    """八字计算接口"""
    _day: LunarDay
    """农历日"""
    _hour: int
    """时"""
    _minute: int
    """分"""
    _second: int
    """秒"""
    _solar_time: SolarTime = None
    """公历时刻（第一次使用时才会初始化）"""
    _sixty_cycle_hour: SixtyCycleHour = None
    """干支时辰（第一次使用时才会初始化）"""

    def __init__(self, year: int, month: int, day: int, hour: int, minute: int = 0, second: int = 0):
        """
        :param year: 农历年，支持从-1到9999年；
        :param month: 农历月，支持1到12，如果为闰月的，使用负数，即-3代表闰三月；
        :param day: 农历日，支持1到30，大月30天，小月29天。
        :param hour: 时为0-23
        :param minute: 分为0-59
        :param second: 秒为0-59
        """
        if hour < 0 or hour > 23:
            raise ValueError(f'illegal hour: {hour}')
        if minute < 0 or minute > 59:
            raise ValueError(f'illegal minute): {minute}')
        if second < 0 or second > 59:
            raise ValueError(f'illegal second: {second}')

        self._day = LunarDay(year, month, day)
        self._hour = hour
        self._minute = minute
        self._second = second

    @classmethod
    def from_ymd_hms(cls, year: int, month: int, day: int, hour: int, minute: int = 0, second: int = 0) -> LunarHour:
        return cls(year, month, day, hour, minute, second)

    def get_lunar_day(self) -> LunarDay:
        """
        :return: 农历日
        """
        return self._day

    def get_year(self) -> int:
        """
        :return: 农历年 number
        """
        return self._day.get_year()

    def get_month(self) -> int:
        """
        :return: 农历月 number
        """
        return self._day.get_month()

    def get_day(self) -> int:
        """
        :return: 农历日 number
        """
        return self._day.get_day()

    def get_hour(self) -> int:
        """
        时
        :return: 返回为数字，范围0到23。
        """
        return self._hour

    def get_minute(self) -> int:
        """
        分
        :return: 返回为数字，范围0到59。
        """
        return self._minute

    def get_second(self) -> int:
        """
        秒
        :return: 返回为数字，范围0到59。
        """
        return self._second

    def get_name(self) -> str:
        from tyme4py.sixtycycle import EarthBranch
        return f'{EarthBranch(self.get_index_in_day()).get_name()}时'

    def __str__(self) -> str:
        return f'{self._day}{self.get_sixty_cycle().get_name()}时'

    def get_index_in_day(self) -> int:
        """
        位于当天的索引
        :return: 数字，范围0到11。
        """
        return int((self._hour + 1) / 2)

    def next(self, n: int) -> LunarHour:
        if n == 0:
            return LunarHour(self.get_year(), self.get_month(), self.get_day(), self._hour, self._minute, self._second)
        h: int = self._hour + n * 2
        diff: int = -1 if h < 0 else 1
        hour: int = abs(h)
        days: int = int(hour / 24) * diff
        hour = (hour % 24) * diff
        if hour < 0:
            hour += 24
            days -= 1
        d: LunarDay = self._day.next(days)
        return LunarHour(d.get_year(), d.get_month(), d.get_day(), hour, self._minute, self._second)

    def is_before(self, target: LunarHour) -> bool:
        """
        是否在指定农历时辰之前
        :param target: 农历时辰
        :return: true/false
        """
        if not self._day == target.get_lunar_day():
            return self._day.is_before(target.get_lunar_day())
        if self._hour != target.get_hour():
            return self._hour < target.get_hour()
        return self._minute < target.get_minute() if self._minute != target.get_minute() else self._second < target.get_second()

    def is_after(self, target: LunarHour) -> bool:
        """
        是否在指定农历时辰之后
        :param target: 农历时辰
        :return: true/false
        """
        if not self._day == target.get_lunar_day():
            return self._day.is_after(target.get_lunar_day())
        if self._hour != target.get_hour():
            return self._hour > target.get_hour()
        return self._minute > target.get_minute() if self._minute != target.get_minute() else self._second > target.get_second()

    def get_year_sixty_cycle(self) -> SixtyCycle:
        """
        当时的年干支  非当时所属的农历年干支
        :return: 干支 SixtyCycle
        """
        warnings.warn('get_year_sixty_cycle() is deprecated, please use SixtyCycleHour.get_year() instead.', DeprecationWarning)
        return self.get_sixty_cycle_hour().get_year()

    def get_month_sixty_cycle(self) -> SixtyCycle:
        """
        当时的月干支 非当天所属的农历月干支，以节令具体时刻换月。
        :return: 干支 SixtyCycle
        """
        warnings.warn('get_year_sixty_cycle() is deprecated, please use SixtyCycleHour.get_month() instead.', DeprecationWarning)
        return self.get_sixty_cycle_hour().get_month()

    def get_day_sixty_cycle(self) -> SixtyCycle:
        """
        当时的日干支
        :return: 干支 SixtyCycle。注意：23:00开始算做第二天。
        """
        warnings.warn('get_year_sixty_cycle() is deprecated, please use SixtyCycleHour.get_day() instead.', DeprecationWarning)
        return self.get_sixty_cycle_hour().get_day()

    def get_sixty_cycle(self) -> SixtyCycle:
        """
        时辰干支
        :return: 干支 SixtyCycle。
        """
        from tyme4py.sixtycycle import SixtyCycle, HeavenStem, EarthBranch
        earth_branch_index: int = self.get_index_in_day() % 12
        d: SixtyCycle = self._day.get_sixty_cycle()
        if self._hour >= 23:
            d = d.next(1)
        return SixtyCycle(HeavenStem(d.get_heaven_stem().get_index() % 5 * 2 + earth_branch_index).get_name() + EarthBranch(earth_branch_index).get_name())

    def get_twelve_star(self) -> TwelveStar:
        """
        :return: 黄道黑道十二神 TwelveStar。
        """
        return TwelveStar(self.get_sixty_cycle().get_earth_branch().get_index() + (8 - self.get_sixty_cycle_hour().get_day().get_earth_branch().get_index() % 6) * 2)

    def get_nine_star(self) -> NineStar:
        """
        九星（时家紫白星歌诀：三元时白最为佳，冬至阳生顺莫差，孟日七宫仲一白，季日四绿发萌芽，每把时辰起甲子，本时星耀照光华，时星移入中宫去，顺飞八方逐细查。夏至阴生逆回首，孟归三碧季加六，仲在九宫时起甲，依然掌中逆轮跨。）
        :return: 九星 NineStar。
        """
        from tyme4py.solar import SolarTerm
        solar: SolarDay = self._day.get_solar_day()
        dong_zhi: SolarTerm = SolarTerm(solar.get_year(), 0)
        earth_branch_index: int = self.get_index_in_day() % 12
        index: int = [8, 5, 2][self._day.get_sixty_cycle().get_earth_branch().get_index() % 3]
        if (not solar.is_before(dong_zhi.get_julian_day().get_solar_day())) and solar.is_before(dong_zhi.next(12).get_julian_day().get_solar_day()):
            index = 8 + earth_branch_index - index
        else:
            index -= earth_branch_index
        return NineStar(index)

    def get_solar_time(self) -> SolarTime:
        """
        公历时刻
        :return: 公历时刻 SolarTime
        """
        from tyme4py.solar import SolarTime
        if self._solar_time is None:
            d: SolarDay = self._day.get_solar_day()
            self._solar_time = SolarTime(d.get_year(), d.get_month(), d.get_day(), self._hour, self._minute, self._second)
        return self._solar_time

    def get_sixty_cycle_hour(self) -> SixtyCycleHour:
        """
        干支时辰
        :return: 干支时辰 SixtyCycleHour
        """
        if self._sixty_cycle_hour is None:
            self._sixty_cycle_hour = self.get_solar_time().get_sixty_cycle_hour()
        return self._sixty_cycle_hour

    def get_eight_char(self) -> EightChar:
        """
        八字
        :return: 八字
        """
        return LunarHour.provider.get_eight_char(self)

    def get_recommends(self) -> list[Taboo]:
        """
        宜
        :return: 宜忌列表
        """
        return Taboo.get_hour_recommends(self.get_sixty_cycle_hour().get_day(), self.get_sixty_cycle())

    def get_avoids(self) -> list[Taboo]:
        """
        忌
        :return: 宜忌列表
        """
        return Taboo.get_hour_avoids(self.get_sixty_cycle_hour().get_day(), self.get_sixty_cycle())

    def get_minor_ren(self) -> MinorRen:
        """
        :return: 小六壬
        """
        return self.get_lunar_day().get_minor_ren().next(self.get_index_in_day())
