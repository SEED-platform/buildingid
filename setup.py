#!/usr/bin/env python3
#
# pnnl-buildingid: setup.py
#
# Copyright (c) 2018, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE.txt and WARRANTY.txt for details.

from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()


def get_version(relpath):
    with open(path.join(here, relpath), encoding="cp437") as f:
        for line in f:
            if "__version__" in line:
                if '"' in line:
                    return line.split('"')[1]
                elif "'" in line:
                    return line.split("'")[1]
    return None


setup(
    name="pnnl-buildingid",
    version=get_version("buildingid/version.py"),
    description="Unique Building Identifier (UBID)",
    long_description=long_description,
    url="https://github.com/pnnl/buildingid",
    author="Mark Borkum",
    author_email="mark.borkum@pnnl.gov",
    license="BSD-2-Clause",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: GIS",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    # keywords=[],
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "click",
        "click_log",
        "openlocationcode",
        "pandas>=2.2.2,<3",
        "pyqtree",
        "shapely",
        "tqdm",
    ],
    setup_requires=[
        "requests",
    ],
    python_requires=">=3",
    extras_require={
        "dev": [
            "check-manifest",
            "coverage",
            "pytest",
            "pytest-cov",
            "pre-commit",
        ],
    },
    entry_points={
        "console_scripts": [
            "buildingid=buildingid.command_line:cli",
        ],
    },
)
