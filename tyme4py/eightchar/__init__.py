# -*- coding:utf-8 -*-
from __future__ import annotations

import warnings
from math import ceil
from typing import TYPE_CHECKING

from tyme4py import AbstractCulture, AbstractTyme
from tyme4py.culture import Duty
from tyme4py.eightchar.provider import ChildLimitProvider
from tyme4py.eightchar.provider.impl import DefaultChildLimitProvider
from tyme4py.enums import Gender, YinYang

if TYPE_CHECKING:
    from tyme4py.lunar import LunarYear
    from tyme4py.solar import SolarTime, SolarTerm, SolarDay
    from tyme4py.sixtycycle import SixtyCycle, SixtyCycleYear, ThreePillars


class EightChar(AbstractCulture):
    """
    八字
    """
    _three_pillars: ThreePillars
    """三柱"""
    _hour: SixtyCycle
    """时柱"""

    def __init__(self, year: SixtyCycle | str, month: SixtyCycle | str, day: SixtyCycle | str, hour: SixtyCycle | str):
        """
        :param year: 年干支
        :param month: 月干支
        :param day: 日干支
        :param hour: 时干支
        """
        from tyme4py.sixtycycle import SixtyCycle, ThreePillars
        self._three_pillars = ThreePillars(year if isinstance(year, SixtyCycle) else SixtyCycle(year), month if isinstance(month, SixtyCycle) else SixtyCycle(month), day if isinstance(day, SixtyCycle) else SixtyCycle(day))
        self._hour = hour if isinstance(hour, SixtyCycle) else SixtyCycle(hour)

    def get_year(self) -> SixtyCycle:
        """
        年柱
        :return: 干支 SixtyCycle
        """
        return self._three_pillars.get_year()

    def get_month(self) -> SixtyCycle:
        """
        月柱
        :return: 干支 SixtyCycle
        """
        return self._three_pillars.get_month()

    def get_day(self) -> SixtyCycle:
        """
        日柱
        :return:  干支 SixtyCycle
        """
        return self._three_pillars.get_day()

    def get_hour(self) -> SixtyCycle:
        """
        时柱
        :return: 干支 SixtyCycle
        """
        return self._hour

    def get_fetal_origin(self) -> SixtyCycle:
        """
        胎元
        :return: 干支 SixtyCycle
        """
        from tyme4py.sixtycycle import SixtyCycle
        m = self.get_month()
        return SixtyCycle(m.get_heaven_stem().next(1).get_name() + m.get_earth_branch().next(3).get_name())

    def get_fetal_breath(self) -> SixtyCycle:
        """
        胎息
        :return: 干支 SixtyCycle
        """
        from tyme4py.sixtycycle import SixtyCycle, EarthBranch
        d = self.get_day()
        return SixtyCycle(d.get_heaven_stem().next(5).get_name() + EarthBranch(13 - d.get_earth_branch().get_index()).get_name())

    def get_own_sign(self) -> SixtyCycle:
        """
        命宫
        :return: 干支 SixtyCycle
        """
        from tyme4py.sixtycycle import SixtyCycle, EarthBranch, HeavenStem
        m: int = self.get_month().get_earth_branch().get_index() - 1
        if m < 1:
            m += 12
        h: int = self._hour.get_earth_branch().get_index() - 1
        if h < 1:
            h += 12
        offset: int = m + h
        offset = (26 if offset >= 14 else 14) - offset
        return SixtyCycle(HeavenStem((self.get_year().get_heaven_stem().get_index() + 1) * 2 + offset - 1).get_name() + EarthBranch(offset + 1).get_name())

    def get_body_sign(self) -> SixtyCycle:
        """
        身宫
        :return: 干支 SixtyCycle
        """
        from tyme4py.sixtycycle import SixtyCycle, EarthBranch, HeavenStem
        offset: int = self.get_month().get_earth_branch().get_index() - 1
        if offset < 1:
            offset += 12
        offset += self._hour.get_earth_branch().get_index() + 1
        if offset > 12:
            offset -= 12
        return SixtyCycle(HeavenStem((self.get_year().get_heaven_stem().get_index() + 1) * 2 + offset - 1).get_name() + EarthBranch(offset + 1).get_name())

    def get_duty(self) -> Duty:
        """
        建除十二值神
        :return: 建除十二值神
        """
        warnings.warn('get_duty() is deprecated, please use SixtyCycleDay.get_duty() instead.', DeprecationWarning)
        return Duty(self.get_day().get_earth_branch().get_index() - self.get_month().get_earth_branch().get_index())

    def get_name(self) -> str:
        return f'{self._three_pillars} {self._hour}'

    def get_solar_times(self, start_year: int, end_year: int) -> list[SolarTime]:
        """
        八字转公历时刻列表
        :param start_year: 开始年份，支持1-9999年
        :param end_year: 结束年份，支持1-9999年
        :return: 公历时刻 SolarTime的列表
        """
        from tyme4py.sixtycycle import HeavenStem
        from tyme4py.solar import SolarTime, SolarTerm
        l: [SolarTime] = []
        year = self.get_year()
        month = self.get_month()
        day = self.get_day()
        # 月地支距寅月的偏移值
        m: int = month.get_earth_branch().next(-2).get_index()
        # 月天干要一致
        if not HeavenStem((year.get_heaven_stem().get_index() + 1) * 2 + m) == month.get_heaven_stem():
            return l

        # 1年的立春是辛酉，序号57
        y: int = year.next(-57).get_index() + 1
        # 节令偏移值
        m *= 2
        # 时辰地支转时刻
        h: int = self._hour.get_earth_branch().get_index() * 2
        # 兼容子时多流派
        hours: [int] = [0, 23] if h == 0 else [h]
        base_year: int = start_year - 1
        if base_year > y:
            y += 60 * int(ceil((base_year - y) / 60.0))

        while y <= end_year:
            # 立春为寅月的开始
            term: SolarTerm = SolarTerm(y, 3)
            # 节令推移，年干支和月干支就都匹配上了
            if m > 0:
                term = term.next(m)

            solar_time: SolarTime = term.get_julian_day().get_solar_time()
            if solar_time.get_year() >= start_year:
                # 日干支和节令干支的偏移值
                solar_day: SolarDay = solar_time.get_solar_day()
                d: int = day.next(-solar_day.get_lunar_day().get_sixty_cycle().get_index()).get_index()
                if d > 0:
                    # 从节令推移天数
                    solar_day = solar_day.next(d)
                for i in range(0, hours.__len__()):
                    mi: int = 0
                    s: int = 0
                    hour: int = hours[i]
                    if d == 0 and hour == solar_time.get_hour():
                        # 如果正好是节令当天，且小时和节令的小时数相等的极端情况，把分钟和秒钟带上
                        mi = solar_time.get_minute()
                        s = solar_time.get_second()

                    time: SolarTime = SolarTime(solar_day.get_year(), solar_day.get_month(), solar_day.get_day(), hour, mi, s)
                    if d == 30:
                        time = time.next(-3600)
                    # 验证一下
                    if time.get_lunar_hour().get_eight_char() == self:
                        l.append(time)
            y += 60
        return l


class ChildLimitInfo:
    """童限信息"""
    _start_time: SolarTime
    """开始(即出生)的公历时刻"""
    _end_time: SolarTime
    """结束(即开始起运)的公历时刻"""
    _year_count: int
    """年数"""
    _month_count: int
    """月数"""
    _day_count: int
    """日数"""
    _hour_count: int
    """小时数"""
    _minute_count: int
    """分钟数"""

    def __init__(self, start_time: SolarTime, end_time: SolarTime, year_count: int, month_count: int, day_count: int, hour_count: int, minute_count: int):
        self._start_time = start_time
        self._end_time = end_time
        self._year_count = year_count
        self._month_count = month_count
        self._day_count = day_count
        self._hour_count = hour_count
        self._minute_count = minute_count

    def get_start_time(self) -> SolarTime:
        """
        :return:  开始(即出生)的公历时刻
        """
        return self._start_time

    def get_end_time(self) -> SolarTime:
        """
        :return: 结束(即开始起运)的公历时刻
        """
        return self._end_time

    def get_year_count(self) -> int:
        """
        :return: 年数
        """
        return self._year_count

    def get_month_count(self) -> int:
        """
        :return: 月数
        """
        return self._month_count

    def get_day_count(self) -> int:
        """
        :return:  日数
        """
        return self._day_count

    def get_hour_count(self) -> int:
        """
        :return: 小时数
        """
        return self._hour_count

    def get_minute_count(self) -> int:
        """
        :return: 分钟数
        """
        return self._minute_count


class ChildLimit:
    """童限（从出生到起运的时间段）"""
    provider: ChildLimitProvider = DefaultChildLimitProvider()
    """童限计算接口"""
    _eight_char: EightChar
    """八字"""
    _gender: Gender
    """性别"""
    _forward: bool
    """顺逆"""
    _info: ChildLimitInfo
    """童限信息"""

    def __init__(self, birth_time: SolarTime, gender: Gender):
        """
        通过出生公历时刻初始化
        :param birth_time: 出生公历时刻
        :param gender: 性别
        """
        self._gender = gender
        self._eight_char = birth_time.get_lunar_hour().get_eight_char()
        # 阳男阴女顺推，阴男阳女逆推
        yang: bool = YinYang.YANG == self._eight_char.get_year().get_heaven_stem().get_yin_yang()
        man: bool = Gender.MAN == gender
        self._forward = (yang and man) or (not yang and not man)
        term: SolarTerm = birth_time.get_term()
        if not term.is_jie():
            term = term.next(-1)
        if self._forward:
            term = term.next(2)
        self._info = ChildLimit.provider.get_info(birth_time, term)

    def get_eight_char(self) -> EightChar:
        """
        :return: 八字
        """
        return self._eight_char

    def get_gender(self) -> Gender:
        """
        :return: 性别
        """
        return self._gender

    def get_year_count(self) -> int:
        """
        :return: 年数
        """
        return self._info.get_year_count()

    def get_month_count(self) -> int:
        """
        :return: 月数
        """
        return self._info.get_month_count()

    def get_day_count(self) -> int:
        """
        :return: 日数
        """
        return self._info.get_day_count()

    def get_hour_count(self) -> int:
        """
        :return: 小时数
        """
        return self._info.get_hour_count()

    def get_minute_count(self) -> int:
        """
        :return: 分钟数
        """
        return self._info.get_minute_count()

    def get_start_time(self) -> SolarTime:
        """
        开始(即出生)的公历时刻
        :return: 公历时刻
        """
        return self._info.get_start_time()

    def get_end_time(self) -> SolarTime:
        """
        结束(即开始起运)的公历时刻
        :return: 公历时刻
        """
        return self._info.get_end_time()

    def is_forward(self) -> bool:
        """
        是否顺推
        :return: true/false
        """
        return self._forward

    def get_start_decade_fortune(self) -> DecadeFortune:
        """
        :return: 起运大运
        """
        return DecadeFortune(self, 0)

    def get_decade_fortune(self) -> DecadeFortune:
        """
        :return: 所属大运
        """
        return DecadeFortune(self, -1)

    def get_start_fortune(self) -> Fortune:
        """
        :return: 小运
        """
        return Fortune(self, 0)

    def get_end_lunar_year(self) -> LunarYear:
        """
        结束农历年
        :return: 农历年
        """
        warnings.warn('get_end_lunar_year() is deprecated, please use SixtyCycleDay.get_duty() instead.', DeprecationWarning)
        from tyme4py.lunar import LunarYear
        return LunarYear.from_year(self.get_start_time().get_lunar_hour().get_year() + self.get_end_time().get_year() - self.get_start_time().get_year())

    def get_start_sixty_cycle_year(self) -> SixtyCycleYear:
        """
        开始(即出生)干支年
        :return: 干支年
        """
        from tyme4py.sixtycycle import SixtyCycleYear
        return SixtyCycleYear.from_year(self.get_start_time().get_year())

    def get_end_sixty_cycle_year(self) -> SixtyCycleYear:
        """
        结束(即起运)干支年
        :return: 干支年
        """
        from tyme4py.sixtycycle import SixtyCycleYear
        return SixtyCycleYear.from_year(self.get_end_time().get_year())

    def get_start_age(self) -> int:
        """
        开始年龄
        :return: 数字
        """
        return 1

    def get_end_age(self) -> int:
        """
        结束年龄
        :return: 数字
        """
        n: int = self.get_end_sixty_cycle_year().get_year() - self.get_start_sixty_cycle_year().get_year()
        return max(n, 1)


class Fortune(AbstractTyme):
    """
    小运--在十年大运中，每一年为一小运。童限结束的公历时刻，既是大运的开始，也是小运的开始。
    """
    _child_limit: ChildLimit
    """童限"""
    _index: int
    """序号"""

    def __init__(self, child_limit: ChildLimit, index: int):
        """
        通过童限初始化
        :param child_limit: 童限
        :param index: 序号
        """
        self._child_limit = child_limit
        self._index = index

    def get_age(self) -> int:
        """
        :return: 年龄
        """
        return self._child_limit.get_end_sixty_cycle_year().get_year() - self._child_limit.get_start_sixty_cycle_year().get_year() + 1 + self._index

    def get_lunar_year(self) -> LunarYear:
        """
        :return: 农历年
        """
        warnings.warn('get_lunar_year() is deprecated, please use get_sixty_cycle_year() instead.', DeprecationWarning)
        return self._child_limit.get_end_lunar_year().next(self._index)

    def get_sixty_cycle_year(self) -> SixtyCycleYear:
        """
        :return: 干支年
        """
        return self._child_limit.get_end_sixty_cycle_year().next(self._index)

    def get_sixty_cycle(self) -> SixtyCycle:
        """
        :return: 干支
        """
        n: int = self.get_age()
        return self._child_limit.get_eight_char().get_hour().next(n if self._child_limit.is_forward() else -n)

    def get_name(self) -> str:
        return self.get_sixty_cycle().get_name()

    def next(self, n: int) -> Fortune:
        return Fortune(self._child_limit, self._index + n)


class DecadeFortune(AbstractTyme):
    """
    大运（10年1大运）--自起运开始，每十年为一大运。童限结束的公历时刻，即开始起运，是大运的开始。
    """
    _child_limit: ChildLimit  # 童限
    _index: int  # 序号

    def __init__(self, child_limit: ChildLimit, index: int):
        """
        通过童限初始化
        :param child_limit: 童限
        :param index: 序号
        """
        self._child_limit = child_limit
        self._index = index

    def get_start_age(self) -> int:
        """
        :return: 开始年龄
        """
        return self._child_limit.get_end_sixty_cycle_year().get_year() - self._child_limit.get_start_sixty_cycle_year().get_year() + 1 + self._index * 10

    def get_end_age(self) -> int:
        """
        :return: 结束年龄
        """
        return self.get_start_age() + 9

    def get_start_lunar_year(self) -> LunarYear:
        """
        开始农历年
        :return: 农历年
        """
        warnings.warn('get_lunar_year() is deprecated, please use get_sixty_cycle_year() instead.', DeprecationWarning)
        return self._child_limit.get_end_lunar_year().next(self._index * 10)

    def get_end_lunar_year(self) -> LunarYear:
        """
        结束农历年
        :return: 农历年
        """
        warnings.warn('get_lunar_year() is deprecated, please use get_sixty_cycle_year() instead.', DeprecationWarning)
        return self.get_start_lunar_year().next(9)

    def get_start_sixty_cycle_year(self) -> SixtyCycleYear:
        """
        开始干支年
        :return: 干支年
        """
        return self._child_limit.get_end_sixty_cycle_year().next(self._index * 10)

    def get_end_sixty_cycle_year(self) -> SixtyCycleYear:
        """
        结束干支年
        :return: 干支年
        """
        return self.get_start_sixty_cycle_year().next(9)

    def get_sixty_cycle(self) -> SixtyCycle:
        """
        :return: 干支
        """
        return self._child_limit.get_eight_char().get_month().next(self._index + 1 if self._child_limit.is_forward() else -self._index - 1)

    def get_name(self) -> str:
        return self.get_sixty_cycle().get_name()

    def next(self, n: int) -> DecadeFortune:
        return DecadeFortune(self._child_limit, self._index + n)

    def get_start_fortune(self) -> Fortune:
        """
        本轮大运中开始的小运
        :return: 小运 Fortune
        """
        return Fortune(self._child_limit, self._index * 10)
