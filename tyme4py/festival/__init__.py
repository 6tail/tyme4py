# -*- coding:utf-8 -*-
from __future__ import annotations

import warnings
from abc import abstractmethod
from typing import TYPE_CHECKING, List, Union

from tyme4py import AbstractTyme, Tyme
from tyme4py.enums import FestivalType, EventType
from tyme4py.event import Event
from tyme4py.unit import DayUnit

if TYPE_CHECKING:
    from tyme4py.lunar import LunarDay
    from tyme4py.solar import SolarTerm, SolarDay


class AbstractFestival(AbstractTyme):
    @abstractmethod
    def next(self, n: int) -> Union[Tyme, None]:
        pass

    def __init__(self, festival_type: FestivalType, index: int, event: Event, day: DayUnit):
        self._type = festival_type
        self._index = index
        self._event = event
        self._day = day

    def get_name(self) -> str:
        return self._event.get_name()

    def get_index(self) -> int:
        """
        :return: 索引
        """
        return self._index

    def get_day(self) -> DayUnit:
        """
        :return: 日
        """
        return self._day

    def get_type(self) -> FestivalType:
        """
        :return: 节日类型
        """
        warnings.warn('get_type() is deprecated.', DeprecationWarning)
        return self._type

    def __str__(self) -> str:
        return f'{self._day} {self.get_name()}'

class LunarFestival(AbstractFestival):
    """
    农历传统节日--依据国家标准《农历的编算和颁行》GB/T 33661-2017
    农历传统节日有：春节、元宵节、龙头节、上巳节、清明节、端午节、七夕节、中元节、中秋节、重阳节、冬至节、腊八节、除夕。
    """
    NAMES: List[str] = ['春节', '元宵节', '龙头节', '上巳节', '清明节', '端午节', '七夕节', '中元节', '中秋节', '重阳节', '冬至节', '腊八节', '除夕']
    """名称"""
    DATA: str = '2VV__0002Vj__0002WW__0002XX__0003b___0002ZZ__0002bb__0002bj__0002cj__0002dd__0003s___0002gc__0002hV_U000'

    def __init__(self, festival_type: FestivalType, index: int, event: Event, day: LunarDay):
        """
        实例化
        :param festival_type: 节日类型
        :param index: 索引
        :param event: 事件
        :param day: 农历日
        """
        super().__init__(festival_type, index, event, day)

    @classmethod
    def from_index(cls, year: int, index: int) -> Union[LunarFestival, None]:
        """
        指定索引得到
        :param year: 年
        :param index: 索引
        :return:
        """
        if index < 0 or index >= cls.NAMES.__len__():
            return None
        from tyme4py.lunar import LunarDay
        from tyme4py.solar import SolarTerm
        start: int = index * 8
        e: Event = Event(LunarFestival.NAMES[index], '@' + LunarFestival.DATA[start: start + 8])
        t: EventType = e.get_type()
        if t == EventType.LUNAR_DAY:
            m: List[int] = e.get_month(year)
            d: LunarDay = LunarDay.from_ymd(m[0], m[1], e.get_value(3))
            offset: int = e.get_value(5)
            return LunarFestival(FestivalType.DAY, index, e, d if offset == 0 else d.next(offset))
        elif t == EventType.TERM_DAY:
            return LunarFestival(FestivalType.TERM, index, e, SolarTerm.from_index(year, e.get_value(2)).get_solar_day().get_lunar_day())
        return None

    @classmethod
    def from_ymd(cls, year: int, month: int, day: int) -> Union[LunarFestival, None]:
        """
        指定农历年、月、日得到
        :param year: 农历年
        :param month: 农历月
        :param day: 农历日
        :return:
        """
        from tyme4py.lunar import LunarDay
        from tyme4py.solar import SolarTermDay
        d: LunarDay = LunarDay.from_ymd(year, month, day)
        for i in range(0, LunarFestival.NAMES.__len__()):
            start: int = i * 8
            e: Event = Event(LunarFestival.NAMES[i], '@' + LunarFestival.DATA[start: start + 8])
            t: EventType = e.get_type()
            if t == EventType.LUNAR_DAY:
                offset: int = e.get_value(5)
                if offset == 0:
                    if d.get_month() == e.get_value(2) and d.get_day() == e.get_value(3):
                      return LunarFestival(FestivalType.DAY, i, e, d)
                else:
                    m: List[int] = e.get_month(d.get_year())
                    n: LunarDay = d.next(-offset)
                    if n.get_year() == m[0] and n.get_month() == m[1] and n.get_day() == e.get_value(3):
                        return LunarFestival(FestivalType.DAY, i, e, d)
            elif t == EventType.TERM_DAY:
                term: SolarTermDay = d.get_solar_day().get_term_day()
                if term.get_day_index() == 0 and term.get_solar_term().get_index() == e.get_value(2) % 24:
                    return LunarFestival(FestivalType.TERM, i, e, d)
        return None

    def get_day(self) -> LunarDay:
        """
        :return: 农历日
        """
        return super().get_day()

    def get_solar_term(self) -> Union[SolarTerm, None]:
        """
        节气，非节气返回None
        :return:  节气
        """
        from tyme4py.solar import SolarTermDay
        t: SolarTermDay = self.get_day().get_solar_day().get_term_day()
        return t.get_solar_term() if t.get_day_index() == 0 else None

    def next(self, n: int) -> LunarFestival:
        size: int = LunarFestival.NAMES.__len__()
        i: int = self._index + n
        return LunarFestival.from_index(int((self._day.get_year() * size + i) / size), self.index_of(i, size))


class SolarFestival(AbstractFestival):
    """公历现代节日"""
    NAMES: List[str] = ['元旦', '妇女节', '植树节', '劳动节', '青年节', '儿童节', '建党节', '建军节', '教师节', '国庆节']
    DATA: str = '0VV__0Ux0Xc__0Ux0Xg__0_Q0ZV__0Ux0ZY__0Ux0aV__0Ux0bV__0Uo0cV__0Ug0de__0_V0eV__0Ux'

    def __init__(self, festival_type: FestivalType, index: int, event: Event, day: SolarDay):
        """
        实例化
        :param festival_type: 节日类型
        :param index: 索引
        :param event: 事件
        :param day: 公历日
        """
        super().__init__(festival_type, index, event, day)

    @classmethod
    def from_index(cls, year: int, index: int) -> Union[SolarFestival, None]:
        """
        指定索引得到
        :param year:  年份
        :param index: 索引
        :return:
        """
        if index < 0 or index >= cls.NAMES.__len__():
            return None
        start: int = index * 8
        e: Event = Event(SolarFestival.NAMES[index], '@' + SolarFestival.DATA[start: start + 8])
        if year < e.get_start_year():
            return None
        from tyme4py.solar import SolarDay
        return SolarFestival(FestivalType.DAY, index, e, SolarDay.from_ymd(year, e.get_value(2), e.get_value(3)))

    @classmethod
    def from_ymd(cls, year: int, month: int, day: int) -> Union[SolarFestival, None]:
        """
        指定年、月、日得到
        :param year:  年
        :param month: 月
        :param day:   日
        :return:
        """
        from tyme4py.solar import SolarDay
        d: SolarDay = SolarDay.from_ymd(year, month, day)
        for i in range(0, SolarFestival.NAMES.__len__()):
            start: int = i * 8
            e: Event = Event(SolarFestival.NAMES[i], '@' + SolarFestival.DATA[start: start + 8])
            if d.get_year() >= e.get_start_year() and d.get_month() == e.get_value(2) and d.get_day() == e.get_value(3):
                return SolarFestival(FestivalType.DAY, i, e, d)
        return None

    def get_day(self) -> SolarDay:
        """
        :return: 公历日
        """
        return super().get_day()

    def get_start_year(self) -> int:
        """
        起始年
        :return: 年
        """
        return self._event.get_start_year()

    def next(self, n: int) -> Union[SolarFestival, None]:
        size: int = SolarFestival.NAMES.__len__()
        i: int = self._index + n
        return SolarFestival.from_index(int((self._day.get_year() * size + i) / size), self.index_of(i, size))
