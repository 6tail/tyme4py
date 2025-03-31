# -*- coding:utf-8 -*-
from __future__ import annotations
from tyme4py import AbstractTyme
from tyme4py.culture import Week
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tyme4py.solar import SolarDay, SolarTime


class JulianDay(AbstractTyme):
    """儒略日"""
    J2000: float = 2451545
    """2000年儒略日数(2000-1-1 12:00:00 UTC)"""
    _day: float
    """儒略日"""

    def __init__(self, day: float):
        """
        :param day: 为小数
        """
        self._day = day

    @classmethod
    def from_julian_day(cls, day: float) -> JulianDay:
        return cls(day)

    @classmethod
    def from_ymd_hms(cls, year: int, month: int, day: int, hour: int, minute: int, second: int) -> JulianDay:
        """
        通过公历年月日时分秒进行初始化
        :param year:  年
        :param month: 月
        :param day:   日
        :param hour:  时
        :param minute: 分
        :param second: 秒
        :return:
        """
        d: float = day + ((second / 60 + minute) / 60 + hour) / 24
        n: int = 0
        g: bool = year * 372 + month * 31 + int(d) >= 588829
        if month <= 2:
            month += 12
            year -= 1
        if g:
            n = int(year / 100)
            n = 2 - n + int(n / 4)
        return cls(int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + d + n - 1524.5)

    def get_day(self) -> float:
        """
        :return: 儒略日
        """
        return self._day

    def get_name(self) -> str:
        return f'{self._day}'

    def next(self, n: float) -> JulianDay:
        return JulianDay(self._day + n)

    def get_solar_day(self) -> SolarDay:
        """
        :return: 公历日
        """
        return self.get_solar_time().get_solar_day()

    def get_solar_time(self) -> SolarTime:
        """
        :return: 公历时刻
        """
        d: int = int(self._day + 0.5)
        f: float = self._day + 0.5 - d
        if d >= 2299161:
            c: int = int((d - 1867216.25) / 36524.25)
            d += 1 + c - int(c / 4)
        d += 1524
        year: int = int((d - 122.1) / 365.25)
        d -= int(365.25 * year)
        month: int = int(d / 30.601)
        d -= int(30.601 * month)
        day: int = d
        if month > 13:
            month -= 13
            year -= 4715
        else:
            month -= 1
            year -= 4716
        f *= 24
        hour: int = int(f)
        f -= hour
        f *= 60
        minute: int = int(f)
        f -= minute
        f *= 60
        second: int = round(f)
        if second > 59:
            second -= 60
            minute += 1
        if minute > 59:
            minute -= 60
            hour += 1
        if hour > 23:
            hour -= 24
            day += 1
        from tyme4py.solar import SolarTime
        return SolarTime(year, month, day, hour, minute, second)

    def get_week(self) -> Week:
        """
        通过儒略日计算的星期是最准的，基姆拉尔森和蔡勒公式计算星期的准确性，在儒略日面前都是弟弟，不服来辩
        :return: 星期
        """
        return Week(int(self._day + 0.5) + 7000001)

    def subtract(self, target: JulianDay) -> float:
        """
        儒略日相减
        :param target: 儒略日
        :return: 差
        """
        return self._day - target.get_day()
