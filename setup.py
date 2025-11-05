from setuptools import setup

setup(
    name='tyme4py',
    version='1.4.0',
    description='Tyme是一个非常强大的日历工具库，可以看作 Lunar 的升级版，拥有更优的设计和扩展性，支持公历、农历、藏历、星座、干支、生肖、节气、法定假日等。',
    long_description='Tyme是一个非常强大的日历工具库，可以看作 Lunar 的升级版，拥有更优的设计和扩展性，支持公历、农历、藏历、星座、干支、生肖、节气、法定假日等。',
    packages=[
        'tyme4py',
        'tyme4py.culture',
        'tyme4py.culture.dog',
        'tyme4py.culture.fetus',
        'tyme4py.culture.nine',
        'tyme4py.culture.pengzu',
        'tyme4py.culture.phenology',
        'tyme4py.culture.plumrain',
        'tyme4py.culture.ren',
        'tyme4py.culture.star',
        'tyme4py.eightchar',
        'tyme4py.eightchar.provider',
        'tyme4py.eightchar.provider.impl',
        'tyme4py.enums',
        'tyme4py.festival',
        'tyme4py.holiday',
        'tyme4py.jd',
        'tyme4py.lunar',
        'tyme4py.sixtycycle',
        'tyme4py.solar',
        'tyme4py.rabbyung',
        'tyme4py.util'
    ],
    url='https://github.com/6tail/tyme4py',
    license='MIT',
    author='6tail',
    author_email='6tail@6tail.cn',
    python_requires='>=3.8.9',
    keywords='公历 农历 藏历 儒略日 星座 干支 节气 法定假日'
)
