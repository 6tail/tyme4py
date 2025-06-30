# -*- coding:utf-8 -*-
import unittest

from tyme4py.eightchar import EightChar, ChildLimit, Fortune, DecadeFortune
from tyme4py.eightchar.provider.impl import China95ChildLimitProvider, LunarSect2EightCharProvider, DefaultEightCharProvider, DefaultChildLimitProvider, LunarSect1ChildLimitProvider, LunarSect2ChildLimitProvider
from tyme4py.enums import Gender
from tyme4py.lunar import LunarHour
from tyme4py.sixtycycle import SixtyCycle, HeavenStem
from tyme4py.solar import SolarTime


class TestEightChar(unittest.TestCase):

    def test1(self):
        """十神"""
        # 八字
        eight_char: EightChar = EightChar(SixtyCycle('丙寅'), SixtyCycle('癸巳'), SixtyCycle('癸酉'), SixtyCycle('己未'))
        # 年柱
        year: SixtyCycle = eight_char.get_year()
        # 月柱
        month: SixtyCycle = eight_char.get_month()
        # 日柱
        day: SixtyCycle = eight_char.get_day()
        # 时柱
        hour: SixtyCycle = eight_char.get_hour()
        # 日元(日主、日干)
        me: HeavenStem = day.get_heaven_stem()
        # 年柱天干十神
        assert me.get_ten_star(year.get_heaven_stem()).get_name() == '正财'
        # 月柱天干十神
        assert me.get_ten_star(month.get_heaven_stem()).get_name() == '比肩'
        # 时柱天干十神
        assert me.get_ten_star(hour.get_heaven_stem()).get_name() == '七杀'
        # 年柱地支十神（本气)
        assert me.get_ten_star(year.get_earth_branch().get_hide_heaven_stem_main()).get_name() == '伤官'
        # 年柱地支十神（中气)
        assert year.get_earth_branch().get_hide_heaven_stem_middle()
        assert me.get_ten_star(year.get_earth_branch().get_hide_heaven_stem_middle()).get_name() == '正财'
        # 年柱地支十神（余气)
        assert year.get_earth_branch().get_hide_heaven_stem_residual()
        assert me.get_ten_star(year.get_earth_branch().get_hide_heaven_stem_residual()).get_name() == '正官'
        # 日柱地支十神（本气)
        assert me.get_ten_star(day.get_earth_branch().get_hide_heaven_stem_main()).get_name() == '偏印'
        # 日柱地支藏干（中气)
        assert day.get_earth_branch().get_hide_heaven_stem_middle() is None
        # 日柱地支藏干（余气)
        assert day.get_earth_branch().get_hide_heaven_stem_residual() is None
        # 指定任意天干的十神
        assert me.get_ten_star(HeavenStem('丙')).get_name() == '正财'

    def test2(self):
        """地势(长生十二神)"""
        # 八字
        eight_char: EightChar = EightChar(SixtyCycle('丙寅'), SixtyCycle('癸巳'), SixtyCycle('癸酉'), SixtyCycle('己未'))
        # 年柱
        year: SixtyCycle = eight_char.get_year()
        # 月柱
        month: SixtyCycle = eight_char.get_month()
        # 日柱
        day: SixtyCycle = eight_char.get_day()
        # 时柱
        hour: SixtyCycle = eight_char.get_hour()
        # 日元(日主、日干)
        me: HeavenStem = day.get_heaven_stem()
        # 年柱地势
        assert me.get_terrain(year.get_earth_branch()).get_name() == '沐浴'
        # 月柱地势
        assert me.get_terrain(month.get_earth_branch()).get_name() == '胎'
        # 日柱地势
        assert me.get_terrain(day.get_earth_branch()).get_name() == '病'
        # 时柱地势
        assert me.get_terrain(hour.get_earth_branch()).get_name() == '墓'

    def test3(self):
        """胎元 / 胎息 / 命宫"""
        # 八字
        eight_char: EightChar = EightChar(SixtyCycle('癸卯'), SixtyCycle('辛酉'), SixtyCycle('己亥'), SixtyCycle('癸酉'))
        # 胎元
        tai_yuan: SixtyCycle = eight_char.get_fetal_origin()
        assert tai_yuan.get_name() == '壬子'
        # 胎元纳音
        assert tai_yuan.get_sound().get_name() == '桑柘木'

    def test4(self):
        """胎息"""
        # 八字
        eight_char: EightChar = EightChar(SixtyCycle('癸卯'), SixtyCycle('辛酉'), SixtyCycle('己亥'), SixtyCycle('癸酉'))
        # 胎息
        tai_xi: SixtyCycle = eight_char.get_fetal_breath()
        assert tai_xi.get_name() == '甲寅'
        # 胎息纳音
        assert tai_xi.get_sound().get_name() == '大溪水'

    def test5(self):
        """命宫"""
        # 八字
        eight_char: EightChar = EightChar(SixtyCycle('癸卯'), SixtyCycle('辛酉'), SixtyCycle('己亥'), SixtyCycle('癸酉'))
        # 命宫
        ming_gong: SixtyCycle = eight_char.get_own_sign()
        assert ming_gong.get_name() == '癸亥'
        # 命宫纳音
        assert ming_gong.get_sound().get_name() == '大海水'

    def test6(self):
        """身宫"""
        # 八字
        eight_char: EightChar = EightChar(SixtyCycle('癸卯'), SixtyCycle('辛酉'), SixtyCycle('己亥'), SixtyCycle('癸酉'))
        # 身宫
        shen_gong: SixtyCycle = eight_char.get_body_sign()
        assert shen_gong.get_name() == '己未'
        # 身宫纳音
        assert shen_gong.get_sound().get_name() == '天上火'

    def test7(self):
        """地势(长生十二神)"""
        # 八字
        eight_char: EightChar = EightChar(SixtyCycle('乙酉'), SixtyCycle('戊子'), SixtyCycle('辛巳'), SixtyCycle('壬辰'))
        # 日干
        me: HeavenStem = eight_char.get_day().get_heaven_stem()
        # 年柱地势
        assert me.get_terrain(eight_char.get_year().get_earth_branch()).get_name() == '临官'
        # 月柱地势
        assert me.get_terrain(eight_char.get_month().get_earth_branch()).get_name() == '长生'
        # 日柱地势
        assert me.get_terrain(eight_char.get_day().get_earth_branch()).get_name() == '死'
        # 时柱地势
        assert me.get_terrain(eight_char.get_hour().get_earth_branch()).get_name() == '墓'

    def test8(self):
        """公历时刻转八字"""
        eight_char: EightChar = SolarTime(2005, 12, 23, 8, 37, 0).get_lunar_hour().get_eight_char()
        assert eight_char.get_year().get_name() == '乙酉'
        assert eight_char.get_month().get_name() == '戊子'
        assert eight_char.get_day().get_name() == '辛巳'
        assert eight_char.get_hour().get_name() == '壬辰'

    def test9(self):
        eight_char: EightChar = SolarTime(1988, 2, 15, 23, 30, 0).get_lunar_hour().get_eight_char()
        assert eight_char.get_year().get_name() == '戊辰'
        assert eight_char.get_month().get_name() == '甲寅'
        assert eight_char.get_day().get_name() == '辛丑'
        assert eight_char.get_hour().get_name() == '戊子'

    def test11(self):
        """童限测试"""
        child_limit: ChildLimit = ChildLimit(SolarTime(2022, 3, 9, 20, 51, 0), Gender.MAN)
        assert child_limit.get_year_count() == 8
        assert child_limit.get_month_count() == 9
        assert child_limit.get_day_count() == 2
        assert child_limit.get_hour_count() == 10
        assert child_limit.get_minute_count() == 6
        assert child_limit.get_end_time().__str__() == '2030年12月12日 06:57:00'

    def test12(self):
        """童限测试"""
        child_limit: ChildLimit = ChildLimit(SolarTime(2018, 6, 11, 9, 30, 0), Gender.WOMAN)
        assert child_limit.get_year_count() == 1
        assert child_limit.get_month_count() == 9
        assert child_limit.get_day_count() == 10
        assert child_limit.get_hour_count() == 1
        assert child_limit.get_minute_count() == 52
        assert child_limit.get_end_time().__str__() == '2020年3月21日 11:22:00'

    def test13(self):
        """大运测试"""
        # 童限
        child_limit: ChildLimit = ChildLimit(SolarTime(1983, 2, 15, 20, 0, 0), Gender.WOMAN)
        # 八字
        assert child_limit.get_eight_char().__str__() == '癸亥 甲寅 甲戌 甲戌'
        # 童限年数
        assert child_limit.get_year_count() == 6
        # 童限月数
        assert child_limit.get_month_count() == 2
        # 童限日数
        assert child_limit.get_day_count() == 18
        # 童限结束(即开始起运)的公历时刻
        assert child_limit.get_end_time().__str__() == '1989年5月4日 18:24:00'
        # 童限开始(即出生)的农历年干支
        assert child_limit.get_start_time().get_lunar_hour().get_lunar_day().get_lunar_month().get_lunar_year().get_sixty_cycle().get_name() == '癸亥'
        # 童限结束(即开始起运)的农历年干支
        assert child_limit.get_end_time().get_lunar_hour().get_lunar_day().get_lunar_month().get_lunar_year().get_sixty_cycle().get_name() == '己巳'
        # 第1轮大运
        decadeFortune: DecadeFortune = child_limit.get_start_decade_fortune()
        # 开始年龄
        assert decadeFortune.get_start_age() == 7
        # 结束年龄
        assert decadeFortune.get_end_age() == 16
        # 开始年
        assert decadeFortune.get_start_sixty_cycle_year().get_year() == 1989
        # 结束年
        assert decadeFortune.get_end_sixty_cycle_year().get_year() == 1998
        # 干支
        assert decadeFortune.get_name() == '乙卯'
        # 下一大运
        assert decadeFortune.next(1).get_name() == '丙辰'
        # 上一大运
        assert decadeFortune.next(-1).get_name() == '甲寅'
        # 第9轮大运
        assert decadeFortune.next(8).get_name() == '癸亥'
        # 小运
        fortune: Fortune = child_limit.get_start_fortune()
        # 年龄
        assert fortune.get_age() == 7
        # 农历年
        assert fortune.get_sixty_cycle_year().get_year() == 1989
        # 干支
        assert fortune.get_name() == '辛巳'
        # 流年
        assert fortune.get_sixty_cycle_year().get_sixty_cycle().get_name() == '己巳'

    def test14(self):
        # 童限
        child_limit: ChildLimit = ChildLimit(SolarTime(1992, 2, 2, 12, 0, 0), Gender.MAN)
        # 八字
        assert child_limit.get_eight_char().__str__() == '辛未 辛丑 戊申 戊午'
        # 童限年数
        assert child_limit.get_year_count() == 9
        # 童限月数
        assert child_limit.get_month_count() == 0
        # 童限日数
        assert child_limit.get_day_count() == 9
        # 童限结束(即开始起运)的公历时刻
        assert child_limit.get_end_time().__str__() == '2001年2月11日 18:58:00'
        # 童限开始(即出生)的农历年干支
        assert child_limit.get_start_time().get_lunar_hour().get_lunar_day().get_lunar_month().get_lunar_year().get_sixty_cycle().get_name() == '辛未'
        # 童限结束(即开始起运)的农历年干支
        assert child_limit.get_end_time().get_lunar_hour().get_lunar_day().get_lunar_month().get_lunar_year().get_sixty_cycle().get_name() == '辛巳'
        # 第1轮大运
        decadeFortune: DecadeFortune = child_limit.get_start_decade_fortune()
        # 开始年龄
        assert decadeFortune.get_start_age() == 10
        # 结束年龄
        assert decadeFortune.get_end_age() == 19
        # 开始年
        assert decadeFortune.get_start_sixty_cycle_year().get_year() == 2001
        # 结束年
        assert decadeFortune.get_end_sixty_cycle_year().get_year() == 2010
        # 干支
        assert decadeFortune.get_name() == '庚子'
        # 下一大运
        assert decadeFortune.next(1).get_name() == '己亥'
        # 小运
        fortune: Fortune = child_limit.get_start_fortune()
        # 年龄
        assert fortune.get_age() == 10
        # 农历年
        assert fortune.get_sixty_cycle_year().get_year() == 2001
        # 干支
        assert fortune.get_name() == '戊申'
        # 小运推移
        assert fortune.next(2).get_name() == '丙午'
        assert fortune.next(-2).get_name() == '庚戌'
        # 流年
        assert fortune.get_sixty_cycle_year().get_sixty_cycle().get_name() == '辛巳'

    def test15(self):
        assert SolarTime(2018, 8, 8, 8, 8, 0).get_lunar_hour().get_eight_char().__str__() == '戊戌 庚申 壬申 甲辰'

    def test16(self):
        # 童限
        child_limit: ChildLimit = ChildLimit(SolarTime(1990, 3, 15, 10, 30, 0), Gender.MAN)
        # 八字
        assert child_limit.get_eight_char().__str__() == '庚午 己卯 己卯 己巳'
        # 童限年数
        assert child_limit.get_year_count() == 6
        # 童限月数
        assert child_limit.get_month_count() == 11
        # 童限日数
        assert child_limit.get_day_count() == 23
        # 童限结束(即开始起运)的公历时刻
        assert child_limit.get_end_time().__str__() == '1997年3月11日 00:22:00'
        # 小运
        fortune: Fortune = child_limit.get_start_fortune()
        # 年龄
        assert fortune.get_age() == 8

    def test17(self):
        eight_char: EightChar = EightChar(SixtyCycle('己丑'), SixtyCycle('戊辰'), SixtyCycle('戊辰'), SixtyCycle('甲子'))
        assert eight_char.get_own_sign().get_name() == '丁丑'

    def test18(self):
        eight_char: EightChar = EightChar(SixtyCycle('戊戌'), SixtyCycle('庚申'), SixtyCycle('丁亥'), SixtyCycle('丙午'))
        assert eight_char.get_own_sign().get_name() == '乙卯'

    def test19(self):
        eight_char: EightChar = EightChar(SixtyCycle('甲子'), SixtyCycle('壬申'), SixtyCycle('庚子'), SixtyCycle('乙亥'))
        assert eight_char.get_own_sign().get_name() == '甲戌'

    def test20(self):
        eight_char: EightChar = ChildLimit(SolarTime(2024, 1, 29, 9, 33, 0), Gender.MAN).get_eight_char()
        assert eight_char.get_own_sign().get_name() == '癸亥'
        assert eight_char.get_body_sign().get_name() == '己未'

    def test21(self):
        eight_char: EightChar = EightChar(SixtyCycle('辛亥'), SixtyCycle('乙未'), SixtyCycle('庚子'), SixtyCycle('甲辰'))
        assert eight_char.get_body_sign().get_name() == '庚子'

    def test22(self):
        assert ChildLimit(SolarTime(1990, 1, 27, 0, 0, 0), Gender.MAN).get_eight_char().get_body_sign().get_name() == '丙寅'

    def test23(self):
        assert ChildLimit(SolarTime(2019, 3, 7, 8, 0, 0), Gender.MAN).get_eight_char().get_own_sign().get_name() == '甲戌'

    def test24(self):
        assert ChildLimit(SolarTime(2019, 3, 27, 2, 0, 0), Gender.MAN).get_eight_char().get_own_sign().get_name() == '丁丑'

    def test25(self):
        assert LunarHour(1994, 5, 20, 18, 0, 0).get_eight_char().get_own_sign().get_name() == '丙寅'

    def test26(self):
        assert SolarTime(1986, 5, 29, 13, 37, 0).get_lunar_hour().get_eight_char().get_body_sign().get_name() == '辛丑'

    def test27(self):
        assert SolarTime(1994, 12, 6, 2, 0, 0).get_lunar_hour().get_eight_char().get_body_sign().get_name() == '丁丑'

    def test28(self):
        eight_char: EightChar = EightChar(SixtyCycle('辛亥'), SixtyCycle('丁酉'), SixtyCycle('丙午'), SixtyCycle('癸巳'))
        assert eight_char.get_own_sign().get_name() == '辛卯'

    def test29(self):
        eight_char: EightChar = EightChar(SixtyCycle('丙寅'), SixtyCycle('庚寅'), SixtyCycle('辛卯'), SixtyCycle('壬辰'))
        assert eight_char.get_own_sign().get_name() == '己亥'
        assert eight_char.get_body_sign().get_name() == '乙未'

    def test30(self):
        assert EightChar('壬子', '辛亥', '壬戌', '乙巳').get_body_sign().get_name() == '乙巳'

    def test31(self):
        # 采用元亨利贞的起运算法
        ChildLimit.provider = China95ChildLimitProvider()
        # 童限
        child_limit: ChildLimit = ChildLimit(SolarTime(1986, 5, 29, 13, 37, 0), Gender.MAN)
        # 童限年数
        assert child_limit.get_year_count() == 2
        # 童限月数
        assert child_limit.get_month_count() == 7
        # 童限日数
        assert child_limit.get_day_count() == 0
        # 童限时数
        assert child_limit.get_hour_count() == 0
        # 童限分数
        assert child_limit.get_minute_count() == 0
        # 童限结束(即开始起运)的公历时刻
        assert child_limit.get_end_time().__str__() == '1988年12月29日 13:37:00'
        # 为了不影响其他测试用例，恢复默认起运算法
        ChildLimit.provider = DefaultChildLimitProvider()

    def test46(self):
        LunarHour.provider = LunarSect2EightCharProvider()
        eight_char: EightChar = EightChar(SixtyCycle('壬寅'), SixtyCycle('丙午'), SixtyCycle('己亥'), SixtyCycle('丙子'))
        time_list: [str] = []
        aa = eight_char.get_solar_times(1900, 2024)
        for time in aa:
            time_list.append(time.__str__())
        assert time_list == ['1962年6月30日 23:00:00', '2022年6月15日 23:00:00']
        LunarHour.provider = DefaultEightCharProvider()

    def test47(self):
        # 采用Lunar流派1的起运算法
        ChildLimit.provider = LunarSect1ChildLimitProvider()
        # 童限
        child_limit: ChildLimit = ChildLimit(SolarTime(1986, 5, 29, 13, 37, 0), Gender.MAN)
        # 童限年数
        assert child_limit.get_year_count() == 2
        # 童限月数
        assert child_limit.get_month_count() == 7
        # 童限日数
        assert child_limit.get_day_count() == 0
        # 童限时数
        assert child_limit.get_hour_count() == 0
        # 童限分数
        assert child_limit.get_minute_count() == 0
        # 童限结束(即开始起运)的公历时刻
        assert child_limit.get_end_time().__str__() == '1988年12月29日 13:37:00'

        # 为了不影响其他测试用例，恢复默认起运算法
        ChildLimit.provider = DefaultChildLimitProvider()

    def test48(self):
        # 采用Lunar流派2的起运算法
        ChildLimit.provider = LunarSect2ChildLimitProvider()
        # 童限
        child_limit: ChildLimit = ChildLimit(SolarTime(1986, 5, 29, 13, 37, 0), Gender.MAN)
        # 童限年数
        assert child_limit.get_year_count() == 2
        # 童限月数
        assert child_limit.get_month_count() == 7
        # 童限日数
        assert child_limit.get_day_count() == 0
        # 童限时数
        assert child_limit.get_hour_count() == 14
        # 童限分数
        assert child_limit.get_minute_count() == 0
        # 童限结束(即开始起运)的公历时刻
        assert child_limit.get_end_time().__str__() == '1988年12月30日 03:37:00'
        # 为了不影响其他测试用例，恢复默认起运算法
        ChildLimit.provider = DefaultChildLimitProvider()

    def test49(self):
        # 采用Lunar流派2的八字算法
        LunarHour.provider = LunarSect2EightCharProvider()
        # 童限
        eight_char: EightChar = LunarHour(2001, 10, 18, 18, 0, 0).get_eight_char()
        assert eight_char.get_name() == '辛巳 己亥 己亥 癸酉'
        # 为了不影响其他测试用例，恢复默认八字算法
        LunarHour.provider = DefaultEightCharProvider()

    def test50(self):
        # 采用Lunar流派2的八字算法
        LunarHour.provider = LunarSect2EightCharProvider()
        # 童限
        eight_char: EightChar = LunarHour(2001, 10, 18, 18, 0, 0).get_eight_char()
        assert eight_char.get_name() == '辛巳 己亥 己亥 癸酉'
        # 为了不影响其他测试用例，恢复默认八字算法
        LunarHour.provider = DefaultEightCharProvider()
