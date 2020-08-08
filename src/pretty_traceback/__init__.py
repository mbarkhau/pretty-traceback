# This file is part of the pretty-traceback project
# https://gitlab.com/mbarkhau/pretty-traceback
#
# Copyright (c) 2020 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT

import os
import sys
import types
import typing as typ
import traceback as tb
import subprocess as sp

import colorama

__version__ = "2020.1003"


def _get_terminal_width() -> int:
    try:
        columns = int(os.environ['COLUMNS'])
        # lines   = int(os.environ['LINES'  ])
        return columns
    except (KeyError, ValueError):
        pass

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
    except IOError:
        pass

    return 0


FMT_MODULE : str = colorama.Fore.CYAN    + colorama.Style.BRIGHT + "{0}" + colorama.Style.RESET_ALL
FMT_CALL   : str = colorama.Fore.YELLOW  + colorama.Style.BRIGHT + "{0}" + colorama.Style.RESET_ALL
FMT_LINENO : str = colorama.Fore.MAGENTA + colorama.Style.BRIGHT + "{0}" + colorama.Style.RESET_ALL
FMT_CONTEXT: str = "{0}"
FMT_ERROR  : str = colorama.Fore.RED + colorama.Style.BRIGHT + "{0}" + colorama.Style.RESET_ALL

Prefix          = str
SectionKey      = typ.Tuple[int, Prefix]
LengthBySection = typ.Dict[SectionKey, int]

Module  = str
LineNo  = str
Call    = str
Context = str

Entry = typ.Tuple[Module, Call, LineNo, Context]
Row   = typ.List[str]
Rows  = typ.List[Row]

SectionRows = typ.Dict[SectionKey, Rows]


class SectionContext(typ.NamedTuple):

    # grouped but unpadded and uncolored
    section_rows: SectionRows

    # paddings
    lbs_module: LengthBySection
    lbs_call  : LengthBySection
    lbs_lineno: LengthBySection


def _init_path_prefixes() -> typ.List[str]:
    _py_paths      = [os.path.abspath(".")] + [os.path.abspath(p) for p in sys.path]
    _uniq_prefixes = {p + os.path.sep for p in _py_paths}
    # Strip the longer prefixes first. This ensures that
    # sub directories are stripped fully.
    return sorted(_uniq_prefixes, key=len, reverse=True)


def _entries_to_sections(entries: typ.Iterable[Entry]) -> SectionContext:
    prefixes = _init_path_prefixes()

    section_rows: typ.Dict[SectionKey, Rows] = {}

    lbs_module: LengthBySection = {}
    lbs_call  : LengthBySection = {}
    lbs_lineno: LengthBySection = {}

    prev_prefix = ""

    for entry in entries:
        module, call, lineno, context = entry

        module_abs_path = os.path.abspath(module)

        prefix          = module
        module_rel_path = ""

        for maybe_prefix in prefixes:
            if module_abs_path.startswith(maybe_prefix):
                prefix          = maybe_prefix
                module_rel_path = module_abs_path.replace(prefix, "", 1)
                break

        if prefix == prev_prefix:
            section_key = (len(section_rows), prefix)
        else:
            section_key = (len(section_rows) + 1, prefix)
            prev_prefix = prefix

        module_padding = lbs_module.get(section_key, 0)
        lbs_module[section_key] = max(module_padding, len(module_rel_path))

        call_padding = lbs_call.get(section_key, 0)
        lbs_call[section_key] = max(call_padding, len(call))

        lineno_padding = lbs_lineno.get(section_key, 0)
        lbs_lineno[section_key] = max(lineno_padding, len(lineno))

        if section_key not in section_rows:
            section_rows[section_key] = []

        section_rows[section_key].append([module_rel_path, call, lineno, context])

    return SectionContext(section_rows, lbs_module, lbs_call, lbs_lineno,)


def _update_padding(ctx: SectionContext) -> None:
    # expand padding from left to right as much as can fit the terminal
    # will mutate section_rows (updating strings with added padding)

    columns = _get_terminal_width()
    for section_key, rows in ctx.section_rows.items():
        section_max_len_module = ctx.lbs_module[section_key]
        section_max_len_call   = ctx.lbs_call[section_key]
        section_max_len_lineno = ctx.lbs_lineno[section_key]

        for row in rows:
            module, call, lineno, context = row
            line_len = 2 + len(module) + 2 + len(call) + 2 + len(lineno) + 2 + len(context)

            padding_available = columns - line_len
            if padding_available <= 0:
                continue

            section_len_module = max(len(module), section_max_len_module)
            padding_consumed   = min(padding_available, section_len_module - len(module))
            row[0] = module.ljust(len(module) + padding_consumed)

            padding_available -= padding_consumed
            if padding_available <= 0:
                continue

            section_len_call = max(len(call), section_max_len_call)
            padding_consumed = min(padding_available, section_len_call - len(call))
            row[1] = call.ljust(len(call) + padding_consumed)

            padding_available -= padding_consumed
            if padding_available <= 0:
                continue

            section_len_lineno = max(len(lineno), section_max_len_lineno)
            padding_consumed   = min(padding_available, section_len_lineno - len(lineno))
            row[2] = lineno.rjust(len(lineno) + padding_consumed)


def _rows_to_lines(section_rows: SectionRows, color: bool = False) -> typ.Iterable[str]:
    # apply colors and additional separators/ spacing
    fmt_module  = FMT_MODULE if color else "{0}"
    fmt_call    = FMT_CALL if color else "{0}"
    fmt_lineno  = FMT_LINENO if color else "{0}"
    fmt_context = FMT_CONTEXT if color else "{0}"

    for (_, prefix), rows in sorted(section_rows.items()):
        yield ""
        yield "  Path: " + fmt_module.format(prefix)

        for module, call, lineno, context in rows:
            parts = (
                "    ",
                fmt_module.format(module),
                "  ",
                fmt_call.format(call),
                "  ",
                fmt_lineno.format(lineno),
                ": ",
                fmt_context.format(context),
            )
            yield "".join(parts)


def format_entries(
    exc_name: str, exc_message: str, entries: typ.List[Entry], color: bool = False
) -> str:
    fmt_error  = FMT_ERROR if color else "{0}"
    error_line = fmt_error.format(exc_name) + ": " + exc_message

    ctx = _entries_to_sections(entries)
    _update_padding(ctx)
    lines = ["Traceback (most recent call last):"]
    lines.extend(_rows_to_lines(ctx.section_rows, color))
    lines.append("")
    lines.append(error_line)
    return os.linesep.join(lines) + os.linesep


def _traceback_to_entries(traceback: types.TracebackType) -> typ.Iterable[Entry]:
    summary = tb.extract_tb(traceback)
    for entry in summary:
        module  = entry[0]
        call    = entry[2]
        lineno  = str(entry[1])
        context = entry[3]
        yield (module, call, lineno, context)


def _exc_to_traceback_str(
    exc_type : typ.Type[BaseException],
    exc_value: BaseException,
    traceback: types.TracebackType,
    color    : bool = False,
) -> str:
    exc_name    = exc_type.__name__
    exc_message = str(exc_value)
    entries     = list(_traceback_to_entries(traceback))
    return format_entries(exc_name, exc_message, entries, color)


def init_excepthook(color: bool) -> typ.Callable:
    def excepthook(
        exc_type: typ.Type[BaseException], exc_value: BaseException, traceback: types.TracebackType
    ) -> None:
        tb_str = _exc_to_traceback_str(exc_type, exc_value, traceback, color)
        try:
            colorama.init()
            sys.stderr.write(tb_str)
        finally:
            colorama.deinit()

    return excepthook


def install(
    envvar                         : typ.Optional[str] = None,
    color                          : bool = True,
    only_tty                       : bool = True,
    only_hook_if_default_excepthook: bool = True,
) -> None:
    """Hook the current excepthook to the pretty_traceback.

    If you set `only_tty=False`, pretty_traceback will always
    be active even when stdout is piped or redirected.
    """
    if envvar and os.environ.get(envvar, "0") == '0':
        return

    isatty = getattr(sys.stderr, 'isatty', lambda: False)
    if only_tty and not isatty():
        return

    if not isatty():
        color = False

    # pylint:disable=comparison-with-callable   ; intentional
    is_default_exepthook = sys.excepthook == sys.__excepthook__
    if only_hook_if_default_excepthook and not is_default_exepthook:
        return

    sys.excepthook = init_excepthook(color=color)


def uninstall() -> None:
    """Restore the default excepthook."""
    sys.excepthook = sys.__excepthook__
