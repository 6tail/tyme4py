# -*- coding:utf-8 -*-
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
