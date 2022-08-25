#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : __init__.py
# Author             : Luis Amilcar Tavares (@mikusher)

import setuptools

long_description = """
<p align="center">
  A python script to automatically get a euro million values.
  <br>
  <a href="https://twitter.com/intent/follow?screen_name=mikusher" title="Follow"></a>
  <br>
</p>
"""

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [x.strip() for x in f.readlines()]

setuptools.setup(
    name="millennium",
    version="1.0",
    description="",
    url="https://github.com/mikusher/scoop",
    author="Mikusher",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email="mikusher@protonmail.com",
    packages=["millennium.src", "src.conf", "src.controller", "src.meta", "src.utils"],
    package_data={'millennium': ['src/dll/']},
    include_package_data=True,
    license="GPL2",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
    entry_points={
        'console_scripts': ['millennium=src.__main__:main']
    }
)
