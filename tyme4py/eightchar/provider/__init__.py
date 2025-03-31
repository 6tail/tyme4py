# -*- coding:utf-8 -*-
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tyme4py.eightchar import EightChar
    from tyme4py.lunar import LunarHour
    from tyme4py.solar import SolarTime, SolarTerm
    from tyme4py.eightchar import ChildLimitInfo


class EightCharProvider(ABC):
    """八字计算接口"""

    @abstractmethod
    def get_eight_char(self, hour: LunarHour) -> EightChar:
        """
        八字
        :param hour: 农历时辰
        :return: 八字 EightChar
        """
        pass


class ChildLimitProvider(ABC):
    """童限计算接口"""

    @abstractmethod
    def get_info(self, birth_time: SolarTime, term: SolarTerm) -> ChildLimitInfo:
        """
        童限信息
        :param birth_time:出生公历时刻
        :param term: 节令
        :return: 童限信息
        """
        pass
