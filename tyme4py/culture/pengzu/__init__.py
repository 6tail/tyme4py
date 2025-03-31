# -*- coding:utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from tyme4py import LoopTyme, AbstractCulture

if TYPE_CHECKING:
    from tyme4py.sixtycycle import SixtyCycle


class PengZuEarthBranch(LoopTyme):
    """地支彭祖百忌"""
    NAMES: [str] = ['子不问卜自惹祸殃', '丑不冠带主不还乡', '寅不祭祀神鬼不尝', '卯不穿井水泉不香', '辰不哭泣必主重丧', '巳不远行财物伏藏', '午不苫盖屋主更张', '未不服药毒气入肠', '申不安床鬼祟入房', '酉不会客醉坐颠狂', '戌不吃犬作怪上床', '亥不嫁娶不利新郎']
    """名称"""

    def __init__(self, index_or_name: int | str):
        super().__init__(self.NAMES, index_or_name)

    @classmethod
    def from_name(cls, name: str) -> PengZuEarthBranch:
        return cls(name)

    @classmethod
    def from_index(cls, index: int) -> PengZuEarthBranch:
        return cls(index)

    def next(self, n: int):
        return PengZuEarthBranch(self.next_index(n))


class PengZuHeavenStem(LoopTyme):
    """天干彭祖百忌"""
    NAMES: [str] = ['甲不开仓财物耗散', '乙不栽植千株不长', '丙不修灶必见灾殃', '丁不剃头头必生疮', '戊不受田田主不祥', '己不破券二比并亡', '庚不经络织机虚张', '辛不合酱主人不尝', '壬不泱水更难提防', '癸不词讼理弱敌强']
    """名称"""

    def __init__(self, index_or_name: int | str):
        super().__init__(self.NAMES, index_or_name)

    @classmethod
    def from_name(cls, name: str) -> PengZuHeavenStem:
        return cls(name)

    @classmethod
    def from_index(cls, index: int) -> PengZuHeavenStem:
        return cls(index)

    def next(self, n: int) -> PengZuHeavenStem:
        return PengZuHeavenStem(self.next_index(n))


class PengZu(AbstractCulture):
    """彭祖百忌"""
    _peng_zu_heaven_stem: PengZuHeavenStem
    """天干彭祖百忌"""
    _peng_zu_earth_branch: PengZuEarthBranch
    """地支彭祖百忌"""

    def __init__(self, sixty_cycle: SixtyCycle):
        self._peng_zu_heaven_stem = PengZuHeavenStem(sixty_cycle.get_heaven_stem().get_index())
        self._peng_zu_earth_branch = PengZuEarthBranch(sixty_cycle.get_earth_branch().get_index())

    @classmethod
    def from_sixty_cycle(cls, sixty_cycle: SixtyCycle) -> PengZu:
        return cls(sixty_cycle)

    def get_name(self) -> str:
        return self._peng_zu_heaven_stem.get_name() + " " + self._peng_zu_earth_branch.get_name()

    def get_peng_zu_heaven_stem(self) -> PengZuHeavenStem:
        """
        天干彭祖百忌
        :return: 天干彭祖百忌
        """
        return self._peng_zu_heaven_stem

    def get_peng_zu_earth_branch(self) -> PengZuEarthBranch:
        """
        地支彭祖百忌
        :return: 地支彭祖百忌
        """
        return self._peng_zu_earth_branch
