# This file is part of the pretty-traceback project
# https://gitlab.com/mbarkhau/pretty-traceback
#
# Copyright (c) 2020 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT

from .hook import install
from .hook import uninstall

__version__ = "2020.1005"


__all__ = [
    'install',
    'uninstall',
    '__version__',
]
