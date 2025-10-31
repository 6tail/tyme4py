# -*- coding:utf-8 -*-
from __future__ import annotations

import re
from typing import TYPE_CHECKING

from tyme4py import AbstractTyme
from tyme4py.enums import FestivalType

if TYPE_CHECKING:
    from tyme4py.lunar import LunarDay
    from tyme4py.solar import SolarTerm, SolarDay


class LunarFestival(AbstractTyme):
    """
    农历传统节日--依据国家标准《农历的编算和颁行》GB/T 33661-2017
    农历传统节日有：春节、元宵节、龙头节、上巳节、清明节、端午节、七夕节、中元节、中秋节、重阳节、冬至节、腊八节、除夕。
    """
    NAMES: [str] = ['春节', '元宵节', '龙头节', '上巳节', '清明节', '端午节', '七夕节', '中元节', '中秋节', '重阳节', '冬至节', '腊八节', '除夕']
    """名称"""
    DATA: str = '@0000101@0100115@0200202@0300303@04107@0500505@0600707@0700715@0800815@0900909@10124@1101208@122'
    _type: FestivalType
    """类型"""
    _index: int
    """索引"""
    _day: LunarDay
    """农历日"""
    _name: str
    """名称"""
    _solar_term: SolarTerm | None
    """节气"""

    def __init__(self, festival_type: FestivalType, day: LunarDay, solar_term: SolarTerm | None, data: str | None = None):
        """
        通过农历日 LunarDay得到
        :param festival_type: 节日类型
        :param day: 农历日
        :param solar_term: 节气
        :param data:
        """
        self._type = festival_type
        self._day = day
        self._solar_term = solar_term
        self._index = int(data[1: 3], 10)
        self._name = LunarFestival.NAMES[self._index]

    @classmethod
    def from_index(cls, year: int, index: int) -> LunarFestival | None:
        """
        指定索引得到
        :param year: 年
        :param index: 索引
        :return:
        """
        if index < 0 or index >= cls.NAMES.__len__():
            raise ValueError(f'illegal index: {index}')
        from tyme4py.lunar import LunarDay
        from tyme4py.solar import SolarTerm
        pattern = re.compile(f"@{index:02}\\d+")
        matcher = pattern.search(cls.DATA)
        if matcher:
            data: str = matcher.group()
            festival_type: int = ord(data[3]) - 48
            if festival_type == 0:
                return cls(FestivalType.DAY, LunarDay(year, int(data[4: 6], 10), int(data[6:], 10)), None, data)
            elif festival_type == 1:
                solar_term: SolarTerm = SolarTerm(year, int(data[4:], 10))
                return cls(FestivalType.TERM, solar_term.get_solar_day().get_lunar_day(), solar_term, data)
            elif festival_type == 2:
                return cls(FestivalType.EVE, LunarDay(year + 1, 1, 1).next(-1), None, data)
            else:
                return None
        return None

    @classmethod
    def from_ymd(cls, year: int, month: int, day: int) -> LunarFestival | None:
        """
        指定农历年、月、日得到
        :param year: 农历年
        :param month: 农历月
        :param day: 农历日
        :return:
        """
        from tyme4py.lunar import LunarDay
        from tyme4py.solar import SolarTerm
        pattern = re.compile("@\\d{2}0" + "{:02}{:02}".format(month, day))
        matcher = pattern.search(cls.DATA)
        if matcher:
            return cls(FestivalType.DAY, LunarDay(year, month, day), None, matcher.group())
        reg = re.compile('@\\d{2}1\\d{2}')
        matcher = reg.search(cls.DATA)
        while matcher:
            data: str = matcher.group()
            solar_term: SolarTerm = SolarTerm(year, int(data[4:], 10))
            lunar_day: LunarDay = solar_term.get_solar_day().get_lunar_day()
            if lunar_day.get_year() == year and lunar_day.get_month() == month and lunar_day.get_day() == day:
                return cls(FestivalType.TERM, lunar_day, solar_term, data)
            last_position = matcher.end()
            matcher = reg.match(cls.DATA, last_position)
        pattern = re.compile("@\\d{2}2")
        matcher = pattern.search(cls.DATA)
        if matcher:
            lunar_day: LunarDay = LunarDay(year, month, day)
            next_day: LunarDay = lunar_day.next(1)
            if next_day.get_month() == 1 and next_day.get_day() == 1:
                return cls(FestivalType.EVE, lunar_day, None, matcher.group())
        return None

    def get_name(self) -> str:
        return self._name

    def get_index(self) -> int:
        """
        :return: 索引
        """
        return self._index

    def get_day(self) -> LunarDay:
        """
        :return: 农历日
        """
        return self._day

    def get_type(self) -> FestivalType:
        """
        :return: 节日类型
        """
        return self._type

    def get_solar_term(self) -> SolarTerm | None:
        """
        节气，非节气返回None
        :return:  节气
        """
        return self._solar_term

    def __str__(self) -> str:
        return f'{self._day} {self._name}'

    def next(self, n: int) -> LunarFestival:
        size: int = LunarFestival.NAMES.__len__()
        i: int = self._index + n
        return LunarFestival.from_index(int((self._day.get_year() * size + i) / size), self.index_of(i, size))


class SolarFestival(AbstractTyme):
    """公历现代节日有：元旦、三八妇女节、植树节、五一劳动节、五四青年节、六一儿童节、建党节、八一建军节、教师节、国庆节。"""
    NAMES: [str] = ['元旦', '三八妇女节', '植树节', '五一劳动节', '五四青年节', '六一儿童节', '建党节', '八一建军节', '教师节', '国庆节']
    DATA: str = '@00001011950@01003081950@02003121979@03005011950@04005041950@05006011950@06007011941@07008011933@08009101985@09010011950'
    _type: FestivalType
    """类型"""
    _index: int
    """索引"""
    _day: SolarDay
    """公历日"""
    _name: str
    """名称"""
    _start_year: int
    """起始年"""

    def __init__(self, festival_type: FestivalType, day: SolarDay, start_year: int, data: str):
        """
        通过公历日 SolarDay得到
        :param festival_type:   节日类型
        :param day: 农历日
        :param start_year: 开始年份
        :param data:
        """
        self._type = festival_type
        self._day = day
        self._start_year = start_year
        self._index = int(data[1: 3], 10)
        self._name = self.NAMES[self._index]

    @classmethod
    def from_index(cls, year: int, index: int) -> SolarFestival | None:
        """
        指定索引得到
        :param year:  年份
        :param index: 索引
        :return:
        """
        if index < 0 or index >= cls.NAMES.__len__():
            raise ValueError(f'illegal index: {index}')
        from tyme4py.solar import SolarDay
        pattern = re.compile(f"@{index:02}\\d+")
        matcher = pattern.search(cls.DATA)
        if matcher:
            data: str = matcher.group()
            type: int = ord(data[3]) - 48
            if type == 0:
                start_year: int = int(data[8:], 10)
                if year >= start_year:
                    return cls(FestivalType.DAY, SolarDay(year, int(data[4: 6], 10), int(data[6: 8], 10)), start_year, data)
        return None

    @classmethod
    def from_ymd(cls, year: int, month: int, day: int) -> SolarFestival | None:
        """
        指定年、月、日得到
        :param year:  年
        :param month: 月
        :param day:   日
        :return:
        """
        from tyme4py.solar import SolarDay
        pattern = re.compile("@\\d{2}0" + f"{month:02}{day:02}\\d+")
        matcher = pattern.search(cls.DATA)
        if matcher:
            data: str = matcher.group()
            start_year: int = int(data[8:], 10)
            if year >= start_year:
                return cls(FestivalType.DAY, SolarDay(year, month, day), start_year, data)
        return None

    def get_name(self) -> str:
        return self._name

    def get_index(self) -> int:
        """
        :return: 索引
        """
        return self._index

    def get_day(self) -> SolarDay:
        """
        :return: 公历日
        """
        return self._day

    def get_type(self) -> FestivalType:
        """
        :return: 节日类型
        """
        return self._type

    def get_start_year(self) -> int:
        """
        起始年
        :return: 年
        """
        return self._start_year

    def __str__(self) -> str:
        return f'{self._day} {self._name}'

    def next(self, n: int) -> SolarFestival | None:
        size: int = SolarFestival.NAMES.__len__()
        i: int = self._index + n
        return SolarFestival.from_index(int((self._day.get_year() * size + i) / size), self.index_of(i, size))
