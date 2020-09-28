# This file is part of the pretty-traceback project
# https://github.com/mbarkhau/pretty-traceback
#
# Copyright (c) 2020 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
import typing as typ


class Entry(typ.NamedTuple):
    module : str
    call   : str
    lineno : str
    src_ctx: str


Entries = typ.List[Entry]


class Traceback(typ.NamedTuple):

    exc_name: str
    exc_msg : str
    entries : Entries

    is_caused : bool
    is_context: bool


Tracebacks = typ.List[Traceback]

ALIASES_HEAD   = "Aliases for entries in sys.path:"
TRACEBACK_HEAD = "Traceback (most recent call last):"
CAUSE_HEAD     = "The above exception was the direct cause of the following exception:"
CONTEXT_HEAD   = "During handling of the above exception, another exception occurred:"
