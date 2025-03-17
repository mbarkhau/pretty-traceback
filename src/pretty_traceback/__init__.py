# This file is part of the pretty-traceback project
# https://github.com/mbarkhau/pretty-traceback
#
# Copyright (c) 2020-2024 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT

from .hook import install
from .hook import uninstall
from .formatting import LoggingFormatter
from .formatting import LoggingFormatterMixin

from ._extension import load_ipython_extension  # noqa: F401

__version__ = "2024.1021"


# retain typo for backward compatibility
LoggingFormaterMixin = LoggingFormatterMixin


__all__ = [
    "install",
    "uninstall",
    "__version__",
    "LoggingFormatter",
    "LoggingFormatterMixin",
    "LoggingFormaterMixin",
]
