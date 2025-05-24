# This file is part of the pretty-traceback project
# https://github.com/mbarkhau/pretty-traceback
#
# Copyright (c) 2020-2024 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT

import os
import re
import sys
import types
import typing as typ
import logging
import traceback as tb
import subprocess as sp
import collections

import colorama

import pretty_traceback.common as com

DEFAULT_COLUMNS = 80


def _get_terminal_width() -> int:
    try:
        columns = int(os.environ['COLUMNS'])
        # lines   = int(os.environ['LINES'  ])
        return columns
    except (KeyError, ValueError):
        pass

    if not sys.stdout.isatty():
        return DEFAULT_COLUMNS

    if hasattr(os, 'get_terminal_size'):
        try:
            size = os.get_terminal_size(0)
            return size.columns
        except OSError:
            pass

    try:
        size_output = sp.check_output(['stty', 'size']).decode()
        _, columns = [int(val) for val in size_output.strip().split()]
        return columns
    except sp.CalledProcessError:
        pass
    except IOError:
        pass

    return DEFAULT_COLUMNS


FMT_MODULE : str = colorama.Fore.CYAN + colorama.Style.NORMAL + "{0}" + colorama.Style.RESET_ALL
FMT_CALL   : str = colorama.Fore.YELLOW + colorama.Style.NORMAL + "{0}" + colorama.Style.RESET_ALL
FMT_LINENO : str = colorama.Fore.MAGENTA + colorama.Style.NORMAL + "{0}" + colorama.Style.RESET_ALL
FMT_CONTEXT: str = "{0}"

FMT_ERROR_NAME: str = colorama.Fore.RED + colorama.Style.BRIGHT + "{0}" + colorama.Style.RESET_ALL
FMT_ERROR_MSG : str = colorama.Style.BRIGHT + "{0}" + colorama.Style.RESET_ALL


class Row(typ.NamedTuple):

    alias       : str
    short_module: str
    full_module : str
    call        : str
    lineno      : str
    context     : str


class PaddedRow(typ.NamedTuple):

    alias       : str
    short_module: str
    full_module : str
    call        : str
    lineno      : str
    context     : str


Alias  = str
Prefix = str

AliasPrefix   = typ.Tuple[Alias, Prefix]
AliasPrefixes = typ.List[AliasPrefix]


class Context(typ.NamedTuple):

    rows   : typ.List[Row]
    aliases: AliasPrefixes

    max_row_width: int
    is_wide_mode : bool

    # for paddings
    max_short_module_len: int
    max_full_module_len : int

    max_lineno_len : int
    max_call_len   : int
    max_context_len: int


def _iter_entry_paths(entries: com.Entries) -> typ.Iterable[str]:
    for entry in entries:
        module_abspath   = os.path.abspath(entry.module)
        is_valid_abspath = module_abspath != entry.module and os.path.exists(module_abspath)
        if is_valid_abspath:
            yield module_abspath
        else:
            yield entry.module


# used by unit tests to override paths
TEST_PATHS: typ.List[str] = []

PWD = os.getcwd()


def _py_paths() -> typ.List[str]:
    if TEST_PATHS:
        return TEST_PATHS

    # NOTE (mb 2020-08-16): We don't know which path entry
    #   was used to import a module. I guess we could figure it
    #   out, but the preference here is to make the shortest
    #   path possible.

    paths = list(sys.path)
    # NOTE (mb 2020-10-04): aliases must be sorted from longest to
    #   shortest, so that the longer matches are used first.
    paths.sort(key=len, reverse=True)

    if "" in paths:
        paths.remove("")

    return paths


def _iter_used_py_paths(entry_paths: typ.List[str]) -> typ.Iterable[str]:
    _uniq_entry_paths = set(entry_paths)

    for py_path in _py_paths():
        is_path_used = False
        for entry_path in list(_uniq_entry_paths):
            if entry_path.startswith(py_path):
                is_path_used = True
                _uniq_entry_paths.remove(entry_path)

        if is_path_used:
            yield py_path


def _iter_alias_prefixes(entry_paths: typ.List[str]) -> typ.Iterable[AliasPrefix]:
    alias_index = 0

    for py_path in _iter_used_py_paths(entry_paths):
        if py_path.endswith("site-packages"):
            alias = "<site>"
        elif py_path.endswith("dist-packages"):
            alias = "<dist>"
        elif re.search(r"lib/python\d.\d+$", py_path):
            alias = "<py>"
        elif re.search(r"lib/Python\d.\d+\\lib$", py_path):
            alias = "<py>"
        elif py_path.startswith(PWD):
            alias   = "<pwd>"
            py_path = PWD
        else:
            alias = f"<p{alias_index}>"
            alias_index += 1

        # Always end paths with a slash. This way relative paths don't
        # start with a / and tooling can open files (e.g. Ctrl+Click),
        # which would otherwise be parsed as absolute paths.
        if not py_path.endswith("/"):
            py_path = py_path + "/"

        yield (alias, py_path)


def _iter_entry_rows(
    aliases: AliasPrefixes, entry_paths: typ.List[str], entries: com.Entries
) -> typ.Iterable[Row]:
    for abs_module, entry in zip(entry_paths, entries):
        used_alias   = ""
        module_full  = abs_module
        module_short = abs_module

        module = entry.module
        if module.startswith("." + os.sep):
            module = module[2:]

        # NOTE (mb 2020-08-18): module may not be an absolute path,
        #   but it's not shortened using an alias yet either.
        if abs_module.endswith(module):
            for alias, alias_path in aliases:
                if abs_module.startswith(alias_path):
                    new_module_short = abs_module[len(alias_path) :]

                    new_len = len(new_module_short) + len(alias)
                    old_len = len(module_short) + len(used_alias)
                    if new_len < old_len:
                        used_alias   = alias
                        module_short = new_module_short

        yield Row(
            used_alias,
            module_short,
            module_full,
            entry.call or "",
            entry.lineno or "",
            entry.src_ctx or "",
        )


def _init_entries_context(entries: com.Entries, term_width: typ.Optional[int] = None) -> Context:
    if term_width is None:
        _term_width = _get_terminal_width()
    else:
        _term_width = term_width

    entry_paths = list(_iter_entry_paths(entries))
    aliases     = list(_iter_alias_prefixes(entry_paths))

    # NOTE (mb 2020-10-04): When calculating widths of a column, we care more
    #   about alignment than staying below the max_row_width. The limits are
    #   only a best effort and padding will be added even if that means
    #   wrapping. We rely on the aliases to reduce the wrapping.

    # indent (4 spaces) + 3 x sep (2 spaces each)
    max_row_width = _term_width - 10

    rows = list(_iter_entry_rows(aliases, entry_paths, entries))

    if rows:
        max_short_module_len = max(len(row.alias) + len(row.short_module) for row in rows)
        max_full_module_len  = max(len(row.full_module) for row in rows)

        max_lineno_len  = max(len(row.lineno) for row in rows)
        max_call_len    = max(len(row.call) for row in rows)
        max_context_len = max(len(row.context) for row in rows)
    else:
        max_short_module_len = 0
        max_full_module_len  = 0

        max_lineno_len  = 0
        max_call_len    = 0
        max_context_len = 0

    max_total_len = max_full_module_len + max_lineno_len + max_call_len + max_context_len
    is_wide_mode  = max_total_len < max_row_width

    return Context(
        rows,
        aliases,
        max_row_width,
        is_wide_mode,
        max_short_module_len,
        max_full_module_len,
        max_lineno_len,
        max_call_len,
        max_context_len,
    )


def _padded_rows(ctx: Context) -> typ.Iterable[PaddedRow]:
    # Expand padding from left to right.
    # This will mutate rows (updating strings with added padding)

    for row in ctx.rows:
        if ctx.is_wide_mode:
            short_module = ""
            full_module  = row.full_module.ljust(ctx.max_full_module_len)
        else:
            short_module = row.short_module.ljust(ctx.max_short_module_len - len(row.alias))
            full_module  = ""

        # the max lengths are calculated upstream in `_init_entries_context`
        padded_call   = row.call.ljust(ctx.max_call_len)
        padded_lineno = row.lineno.ljust(ctx.max_lineno_len)

        yield PaddedRow(
            row.alias,
            short_module,
            full_module,
            padded_call,
            padded_lineno,
            row.context,
        )


def _aliases_to_lines(ctx: Context, color: bool = False) -> typ.Iterable[str]:
    fmt_module = FMT_MODULE if color else "{0}"
    if ctx.aliases:
        alias_padding = max(len(alias) for alias, _ in ctx.aliases)
        for alias, path in ctx.aliases:
            yield "    " + alias.ljust(alias_padding) + ": " + fmt_module.format(path)


def _rows_to_lines(rows: typ.List[PaddedRow], color: bool = False) -> typ.Iterable[str]:

    # apply colors and additional separators/ spacing
    fmt_module  = FMT_MODULE if color else "{0}"
    fmt_call    = FMT_CALL if color else "{0}"
    fmt_lineno  = FMT_LINENO if color else "{0}"
    fmt_context = FMT_CONTEXT if color else "{0}"

    # padding has already been added to the components at this point
    for alias, short_module, full_module, call, lineno, context in rows:
        if short_module:
            _alias = alias
            module = short_module
        else:
            _alias = ""
            module = full_module

        # append line number to file so editors can jump to the line
        bare_module    = module.strip()
        bare_lineno    = lineno.strip()
        module_padding = " " * (len(module) - len(bare_module) + len(lineno) - len(bare_lineno))

        parts = (
            "    ",
            _alias,
            " ",
            fmt_module.format(bare_module),
            ":",
            fmt_lineno.format(bare_lineno),
            module_padding,
            "  ",
            fmt_call.format(call),
            "  ",
            fmt_context.format(context),
        )

        line = "".join(parts)

        if alias == "<pwd>":
            yield line.replace(colorama.Style.NORMAL, colorama.Style.BRIGHT)
        else:
            yield line


def _traceback_to_entries(traceback: types.TracebackType) -> typ.Iterable[com.Entry]:
    summary = tb.extract_tb(traceback)
    for entry in summary:
        module  = entry[0]
        call    = entry[2]
        lineno  = str(entry[1])
        context = entry[3] or ""
        yield com.Entry(module, call, lineno, context)


def _format_traceback(ctx: Context, traceback: com.Traceback, color: bool = False) -> str:
    padded_rows = list(_padded_rows(ctx))

    lines = []
    if ctx.aliases and not ctx.is_wide_mode:
        lines.append(com.ALIASES_HEAD)
        lines.extend(_aliases_to_lines(ctx, color))

    lines.append(com.TRACEBACK_HEAD)
    lines.extend(_rows_to_lines(padded_rows, color))

    if traceback.exc_name == 'RecursionError' and len(lines) > 100:
        prelude_index = 0

        line_counts: typ.Dict[str, int] = collections.defaultdict(int)
        for i, line in enumerate(lines):
            line_counts[line] += 1
            if line_counts[line] == 3:
                prelude_index = i
                break

        if prelude_index > 0:
            num_omitted = len(lines) - prelude_index - 2
            lines       = lines[:prelude_index] + [f"    ... {num_omitted} omitted lines"] + lines[-2:]

    fmt_error_name = FMT_ERROR_NAME if color else "{0}"
    error_line     = fmt_error_name.format(traceback.exc_name)
    if traceback.exc_msg:
        fmt_error_msg = FMT_ERROR_MSG if color else "{0}"
        error_line += ": " + fmt_error_msg.format(traceback.exc_msg)

    lines.append(error_line)
    return os.linesep.join(lines) + os.linesep


def format_traceback(traceback: com.Traceback, color: bool = False) -> str:
    ctx = _init_entries_context(traceback.entries)
    return _format_traceback(ctx, traceback, color)


def format_tracebacks(tracebacks: typ.List[com.Traceback], color: bool = False) -> str:
    traceback_strs: typ.List[str] = []

    for tb_tup in tracebacks:
        if tb_tup.is_caused:
            # traceback_strs.append("vvv caused by ^^^ - ")
            traceback_strs.append(com.CAUSE_HEAD + os.linesep)
        elif tb_tup.is_context:
            # traceback_strs.append("vvv happend after ^^^ - ")
            traceback_strs.append(com.CONTEXT_HEAD + os.linesep)

        traceback_str = format_traceback(tb_tup, color)
        traceback_strs.append(traceback_str)

    return os.linesep.join(traceback_strs).strip()


def get_tb_attr(ex: BaseException) -> types.TracebackType:
    return typ.cast(types.TracebackType, getattr(ex, '__traceback__', None))


def exc_to_traceback_str(
    exc_value: BaseException,
    traceback: types.TracebackType,
    color    : bool = False,
) -> str:
    # NOTE (mb 2020-08-13): wrt. cause vs context see
    #   https://www.python.org/dev/peps/pep-3134/#enhanced-reporting
    #   https://stackoverflow.com/questions/11235932/
    tracebacks: typ.List[com.Traceback] = []

    cur_exc_value: BaseException = exc_value
    cur_traceback: types.TracebackType = traceback

    while cur_exc_value:
        next_cause   = getattr(cur_exc_value, '__cause__', None)
        next_context = getattr(cur_exc_value, '__context__', None)

        tb_tup = com.Traceback(
            exc_name=type(cur_exc_value).__name__,
            exc_msg=str(cur_exc_value),
            entries=list(_traceback_to_entries(cur_traceback)),
            is_caused=bool(next_cause),
            is_context=bool(next_context),
        )

        tracebacks.append(tb_tup)

        if next_cause:
            cur_exc_value = next_cause
            cur_traceback = get_tb_attr(next_cause)
        elif next_context:
            cur_exc_value = next_context
            cur_traceback = get_tb_attr(next_context)
        else:
            break

    tracebacks = list(reversed(tracebacks))

    return format_tracebacks(tracebacks, color)


class LoggingFormatterMixin:
    # pylint:disable=invalid-name   # logging module naming convention
    # pylint:disable=no-self-use    # because mixin

    def formatException(self, ei) -> str:
        _, exc_value, traceback = ei
        return exc_to_traceback_str(exc_value, traceback, color=True)


class LoggingFormatter(LoggingFormatterMixin, logging.Formatter):

    pass
