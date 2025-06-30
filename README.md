# Tyme [![License](https://img.shields.io/badge/license-MIT-4EB1BA.svg?style=flat-square)](https://github.com/6tail/tyme4py/blob/master/LICENSE)

Tyme是一个非常强大的日历工具库，可以看作 [Lunar](https://6tail.cn/calendar/api.html "https://6tail.cn/calendar/api.html") 的升级版，拥有更优的设计和扩展性，支持公历、农历、藏历、星座、干支、生肖、节气、法定假日等。

> 基于python3.8.9开发

## 示例

    $ pip install tyme4py
     
    from tyme4py.solar import SolarDay
     
    # 通过指定年月日初始化公历日
    solar_day = SolarDay.from_ymd(1986, 5, 29)
     
    # 1986年5月29日
    print(solar_day.__str__())
     
    # 农历丙寅年四月廿一
    print(solar_day.get_lunar_day().__str__())
     
    # 第十七饶迥火虎年四月廿一
    print(solar_day.get_rab_byung_day().__str__())

## 文档

请移步至 [https://6tail.cn/tyme.html](https://6tail.cn/tyme.html "https://6tail.cn/tyme.html")

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=6tail/tyme4py&type=Date)](https://star-history.com/#6tail/tyme4py&Date)

## 致谢
1. 感谢许剑伟老师分享的寿星天文历，本项目节气算法引自 [https://github.com/sxwnl/sxwnl](https://github.com/sxwnl/sxwnl "https://github.com/sxwnl/sxwnl")
2. 感谢[stonelf](https://github.com/stonelf "https://github.com/stonelf")，本项目藏历数据引自 [https://github.com/stonelf/zangli](https://github.com/stonelf/zangli "https://github.com/stonelf/zangli")
