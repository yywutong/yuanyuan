#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
@Author: zhoushuke
@Email: zhoushuke@sensetime.com
@Date: 2020-04-24 14:14:02
LastEditors: zhoushuke
LastEditTime: 2021-04-26 17:03:02
FilePath: /fallen_deliver/setup.py
'''

from pathlib import Path
from setuptools import find_packages, setup


def load_requirements(filename):
    with Path(filename).open() as reqfile:
        return [line.strip() for line in reqfile if not line.startswith("#")]


# Populates __version__ without importing the package
__version__ = None
with open("fallendeliver/__version__.py", encoding="utf-8") as ver_file:
    exec(ver_file.read())  # pylint: disable=W0122

if not __version__:
    print("Could not find __version__ from fallendeliver/__version__.py")
    exit(1)

setup(
    name='fallendeliver',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=load_requirements("requirements.txt"),
    python_requires=">=3.6",
)
