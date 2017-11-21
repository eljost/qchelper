#!/usr/bin/env python3

from setuptools import find_packages, setup
import sys

if sys.version_info.major < 3:
    raise SystemExit("Python 3 is required!")

setup(
    name="qchelper",
    version="0.0.1",
    description="Helper functions for working with quantum chemistry data.",
    url="https://github.com/eljost/qchelper",
    maintainer="Johannes Steinmetzer",
    maintainer_email="johannes.steinmetzer@uni-jena.de",
    license="GPL 3",
    platforms=["unix"],
    packages=find_packages(),
    install_requires=[
        "scipy",
        "numpy",
        "matplotlib",
        "chemcoord",
        "pandas",
        "simplejson",
        "brewer2mpl",
        "jinja2",
        "natsort",
    ],
)
