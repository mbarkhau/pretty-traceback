# This file is part of the pretty-traceback project
# https://github.com/mbarkhau/pretty-traceback
#
# Copyright (c) 2020 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT

import os
import sys
import setuptools


def project_path(*sub_paths):
    project_dirpath = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(project_dirpath, *sub_paths)


def read(*sub_paths):
    with open(project_path(*sub_paths), mode="rb") as fh:
        return fh.read().decode("utf-8")


install_requires = [
    line.strip()
    for line in read("requirements", "pypi.txt").splitlines()
    if line.strip() and not line.startswith("#") and not line.startswith("-")
]


long_description = "\n\n".join((read("README.md"), read("CHANGELOG.md")))


# See https://pypi.python.org/pypi?%3Aaction=list_classifiers
classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Environment :: Other Environment",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: Unix",
    "Operating System :: POSIX",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Python Modules",
]


try:
    import lib3to6
    distclass = lib3to6.Distribution
except ImportError:
    distclass = setuptools.dist.Distribution


setuptools.setup(
    name="pretty-traceback",
    license="MIT",
    author="Manuel Barkhau",
    author_email="mbarkhau@gmail.com",
    url="https://github.com/mbarkhau/pretty-traceback",
    version="2022.1018",
    keywords="traceback stacktrace pretty",
    description="Human readable stacktraces.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    distclass=distclass,
    packages=setuptools.find_packages("src/"),
    package_dir={"": "src"},
    install_requires=install_requires,
    python_requires=">=2.7",
    zip_safe=True,
    classifiers=classifiers,
)
