# This file is part of the pretty-traceback project
# https://github.com/mbarkhau/pretty-traceback
#
# Copyright (c) 2020-2023 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT

from .hook import install
from .hook import uninstall
from .formatting import LoggingFormatter
from .formatting import LoggingFormatterMixin

__version__ = "2023.1020"


# retain typo for backward compatibility
LoggingFormaterMixin = LoggingFormatterMixin


__all__ = [
    'install',
    'uninstall',
    '__version__',
    'LoggingFormatter',
    'LoggingFormatterMixin',
    'LoggingFormaterMixin',
]
