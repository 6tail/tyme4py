# -*- coding:utf-8 -*-
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from tyme4py.eightchar.provider import EightCharProvider, ChildLimitProvider

if TYPE_CHECKING:
    from tyme4py.eightchar import EightChar, ChildLimitInfo
    from tyme4py.lunar import LunarHour
    from tyme4py.solar import SolarTime, SolarTerm, SolarMonth


class DefaultEightCharProvider(EightCharProvider):
    """默认的八字计算（晚子时算第二天）"""

    def get_eight_char(self, hour: LunarHour) -> EightChar:
        return hour.get_sixty_cycle_hour().get_eight_char()


class LunarSect2EightCharProvider(EightCharProvider):
    """Lunar流派2的八字计算（晚子时日柱算当天）"""

    def get_eight_char(self, hour: LunarHour) -> EightChar:
        from tyme4py.eightchar import EightChar
        from tyme4py.sixtycycle import SixtyCycleHour
        h: SixtyCycleHour = hour.get_sixty_cycle_hour()
        return EightChar(h.get_year(), h.get_month(), hour.get_lunar_day().get_sixty_cycle(), h.get_sixty_cycle())


class AbstractChildLimitProvider(ChildLimitProvider):
    """童限计算抽象"""

    @staticmethod
    def next(birth_time: SolarTime, add_year: int, add_month: int, add_day: int, add_hour: int, add_minute: int, add_second: int) -> ChildLimitInfo:
        from tyme4py.solar import SolarTime, SolarMonth
        from tyme4py.eightchar import ChildLimitInfo
        d: int = birth_time.get_day() + add_day
        h: int = birth_time.get_hour() + add_hour
        mi: int = birth_time.get_minute() + add_minute
        s: int = birth_time.get_second() + add_second
        mi += s // 60
        s %= 60
        h += mi // 60
        mi %= 60
        d += h // 24
        h %= 24
        sm: SolarMonth = SolarMonth(birth_time.get_year() + add_year, birth_time.get_month()).next(add_month)
        dc: int = sm.get_day_count()
        while d > dc:
            d -= dc
            sm = sm.next(1)
            dc = sm.get_day_count()
        return ChildLimitInfo(birth_time, SolarTime(sm.get_year(), sm.get_month(), d, h, mi, s), add_year, add_month, add_day, add_hour, add_minute)

    @abstractmethod
    def get_info(self, birth_time: SolarTime, term: SolarTerm) -> ChildLimitInfo:
        pass


class DefaultChildLimitProvider(AbstractChildLimitProvider):
    """默认的八字计算（晚子时算第二天）"""

    def get_info(self, birth_time: SolarTime, term: SolarTerm) -> ChildLimitInfo:
        # 出生时刻和节令时刻相差的秒数
        seconds: int = abs(term.get_julian_day().get_solar_time().subtract(birth_time))
        # 3天 = 1年，3天=60*60*24*3秒=259200秒 = 1年
        year: int = seconds // 259200
        seconds %= 259200
        # 1天 = 4月，1天=60*60*24秒=86400秒 = 4月，85400秒/4=21600秒 = 1月
        month: int = seconds // 21600
        seconds %= 21600
        # 1时 = 5天，1时=60*60秒=3600秒 = 5天，3600秒/5=720秒 = 1天
        day: int = seconds // 720
        seconds %= 720
        # 1分 = 2时，60秒 = 2时，60秒/2=30秒 = 1时
        hour: int = seconds // 30
        seconds %= 30
        # 1秒 = 2分，1秒/2=0.5秒 = 1分
        minute: int = seconds * 2
        return AbstractChildLimitProvider.next(birth_time, year, month, day, hour, minute, 0)


class China95ChildLimitProvider(AbstractChildLimitProvider):
    """元亨利贞的童限计算"""

    def get_info(self, birth_time: SolarTime, term: SolarTerm) -> ChildLimitInfo:
        # 出生时刻和节令时刻相差的分钟数
        minutes: int = int(abs(term.get_julian_day().get_solar_time().subtract(birth_time)) / 60)
        year: int = minutes // 4320
        minutes %= 4320
        month: int = minutes // 360
        minutes %= 360
        day: int = minutes // 12
        return AbstractChildLimitProvider.next(birth_time, year, month, day, 0, 0, 0)


class LunarSect1ChildLimitProvider(AbstractChildLimitProvider):
    """Lunar的流派1童限计算（按天数和时辰数计算，3天1年，1天4个月，1时辰10天）"""

    def get_info(self, birth_time: SolarTime, term: SolarTerm) -> ChildLimitInfo:
        term_time: SolarTime = term.get_julian_day().get_solar_time()
        end: SolarTime = term_time
        start: SolarTime = birth_time
        if birth_time.is_after(term_time):
            end = birth_time
            start = term_time

        end_time_zhi_index: int = 11 if end.get_hour() == 23 else end.get_lunar_hour().get_index_in_day()
        start_time_zhi_index: int = 11 if start.get_hour() == 23 else start.get_lunar_hour().get_index_in_day()
        # 时辰差
        hour_diff: int = end_time_zhi_index - start_time_zhi_index
        # 天数差
        day_diff: int = end.get_solar_day().subtract(start.get_solar_day())
        if hour_diff < 0:
            hour_diff += 12
            day_diff -= 1

        month_diff: int = int(hour_diff * 10 / 30)
        month: int = day_diff * 4 + month_diff
        day: int = hour_diff * 10 - month_diff * 30
        year: int = int(month / 12)
        month = month - year * 12
        return AbstractChildLimitProvider.next(birth_time, year, month, day, 0, 0, 0)


class LunarSect2ChildLimitProvider(AbstractChildLimitProvider):
    """Lunar的流派2童限计算（按分钟数计算）"""

    def get_info(self, birth_time: SolarTime, term: SolarTerm) -> ChildLimitInfo:
        # 出生时刻和节令时刻相差的分钟数
        minutes: int = int(abs(term.get_julian_day().get_solar_time().subtract(birth_time)) / 60)
        year: int = int(minutes / 4320)
        minutes %= 4320
        month: int = int(minutes / 360)
        minutes %= 360
        day: int = int(minutes / 12)
        minutes %= 12
        hour: int = minutes * 2
        return AbstractChildLimitProvider.next(birth_time, year, month, day, hour, 0, 0)
