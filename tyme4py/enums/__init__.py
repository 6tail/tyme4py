# -*- coding:utf-8 -*-
import warnings
from enum import Enum


class YinYang(Enum):
    """阴阳：YIN=0=阴，YANG=1=阳"""
    YIN = 0
    """阴"""
    YANG = 1
    """阳"""


class Side(Enum):
    """内外：IN=0=内，OUT=1=外"""
    IN = 0
    """内"""
    OUT = 1
    """外"""


class Gender(Enum):
    """性别：WOMAN=0=女，MAN=1=男"""
    WOMAN = 0
    """女"""
    MAN = 1
    """男"""


class FestivalType(Enum):
    """节日类型：DAY=0=日期，TERM=1=节气，EVE=2=除夕"""
    warnings.warn('FestivalType is deprecated.', DeprecationWarning)
    DAY = 0
    """日期"""
    TERM = 1
    """节气"""
    EVE = 2
    """除夕"""


class HideHeavenStemType(Enum):
    """藏干类型：RESIDUAL=0=余气，MIDDLE=1=中气，MAIN=2=本气"""
    RESIDUAL = 0
    """余气"""
    MIDDLE = 1
    """中气"""
    MAIN = 2
    """本气"""


class EventType(Enum):
    """事件类型"""
    SOLAR_DAY = 0
    """公历日期"""
    SOLAR_WEEK = 1
    """几月第几个星期几"""
    LUNAR_DAY = 2
    """农历日期"""
    TERM_DAY = 3
    """节气日期"""
    TERM_HS = 4
    """节气天干"""
    TERM_EB = 5
    """节气地支"""
