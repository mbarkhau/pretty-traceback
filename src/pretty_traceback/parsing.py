# This file is part of the pretty-traceback project
# https://github.com/mbarkhau/pretty-traceback
#
# Copyright (c) 2020 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT

import re
import typing as typ

import pretty_traceback.common as com

# TODO (mb 2020-08-12): path/module with doublequotes in them.
#   Not even sure what python does with that.

# https://regex101.com/r/GpKtqR/1
LOCATION_PATTERN = r"""
\s\s
File
    \s
        \"(?P<module>[^\"]+)\"
    ,\sline\s
        (?P<lineno>\d+)
    ,\sin\s
        (?P<call>.*)
"""
LOCATION_RE = re.compile(LOCATION_PATTERN, flags=re.VERBOSE)


def _parse_entries(entry_lines: typ.List[str]) -> typ.Iterable[com.Entry]:
    i = 0
    while i < len(entry_lines):
        line = entry_lines[i]
        i += 1
        loc_match = LOCATION_RE.match(line)
        if loc_match is None:
            continue

        if i < len(entry_lines):
            maybe_src_ctx = entry_lines[i]
        else:
            maybe_src_ctx = ""

        is_src_ctx = maybe_src_ctx.startswith("    ")
        if is_src_ctx:
            src_ctx = maybe_src_ctx.strip()
            i += 1
        else:
            src_ctx = ""

        module, lineno, call = loc_match.groups()

        yield com.Entry(module, call, lineno, src_ctx)


TRACE_HEADERS = {com.TRACEBACK_HEAD, com.CAUSE_HEAD, com.CONTEXT_HEAD}


def _iter_tracebacks(trace: str) -> typ.Iterable[com.Traceback]:
    lines = trace.strip().splitlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # skip empty lines
        if not line:
            i += 1
            continue

        is_caused  = False
        is_context = False

        if line.startswith(com.CAUSE_HEAD):
            is_caused = True
            i += 1
        elif line.startswith(com.CONTEXT_HEAD):
            is_context = True
            i += 1

        # skip empty lines and tb head
        while i < len(lines):
            line = lines[i].strip()
            if not line or line.startswith(com.TRACEBACK_HEAD):
                i += 1
            else:
                break

        # accumulate entry lines
        entry_lines: typ.List[str] = []
        while i < len(lines) and lines[i].startswith("  "):
            entry_lines.append(lines[i])
            i += 1

        exc_line = lines[i]
        if ": " in exc_line:
            exc_name, exc_msg = exc_line.split(": ", 1)
        else:
            exc_name = exc_line
            exc_msg  = ""

        entries = list(_parse_entries(entry_lines))
        yield com.Traceback(
            exc_name=exc_name,
            exc_msg=exc_msg,
            entries=entries,
            is_caused=is_caused,
            is_context=is_context,
        )

        i += 1


def parse_tracebacks(trace: str) -> com.Tracebacks:
    """Parses a chain of tracebacks.

    Args:
        trace: The traceback in the default python format, starting with
                   "Traceback (most recent call last):"
               ending with the last line in the chain, e.g.
                   "FileNotFoundError: [Errno 2] No such ..."
    """
    return list(_iter_tracebacks(trace))
