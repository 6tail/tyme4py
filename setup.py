from setuptools import setup, find_packages
import re
from pathlib import Path

# Read version from tyme4py/__init__.py
def get_version():
    init_file = Path(__file__).parent / 'tyme4py' / '__init__.py'
    content = init_file.read_text(encoding='utf-8')
    match = re.search(r"^__version__\s*=\s*['\"]([^'\"]+)['\"]", content, re.M)
    if match:
        return match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='tyme4py',
    version=get_version(),
    description='Tyme是一个非常强大的日历工具库，可以看作 Lunar 的升级版，拥有更优的设计和扩展性，支持公历、农历、藏历、星座、干支、生肖、节气、法定假日等。',
    long_description='Tyme是一个非常强大的日历工具库，可以看作 Lunar 的升级版，拥有更优的设计和扩展性，支持公历、农历、藏历、星座、干支、生肖、节气、法定假日等。',
    packages=find_packages(exclude=['test', 'test.*']),
    url='https://github.com/6tail/tyme4py',
    author='6tail',
    author_email='6tail@6tail.cn',
    python_requires='>=3.10',
    keywords='公历 农历 藏历 儒略日 星座 干支 节气 法定假日',
    include_package_data=True
)
