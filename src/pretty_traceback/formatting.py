# This file is part of the pretty-traceback project
# https://gitlab.com/mbarkhau/pretty-traceback
#
# Copyright (c) 2020 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT

import os
import re
import sys
import types
import typing as typ
import traceback as tb
import subprocess as sp
import collections

import colorama

import pretty_traceback.common as com


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

Row  = typ.List[str]
Rows = typ.List[Row]


Alias         = str
Prefix        = str
AliasPrefixes = typ.List[typ.Tuple[Alias, Prefix]]


class Context(typ.NamedTuple):

    rows   : Rows
    aliases: AliasPrefixes

    # for paddings
    max_module_len: int
    max_lineno_len: int
    max_call_len  : int


PYTHON_ENV_PATTERN = r"""
(?P<prefix>.*[Pp]ython(?P<version>[\d\.]+))
(?P<suffix>.*)
"""
PYTHON_ENV_RE = re.compile(PYTHON_ENV_PATTERN, flags=re.VERBOSE)


WINPATH_RE = re.compile(r"^[a-z]:\\", flags=re.IGNORECASE)

assert WINPATH_RE.match("c:\\users\\")
assert WINPATH_RE.match("C:\\Users\\usrna")

assert WINPATH_RE.match(".\\src\\libname") is None
assert WINPATH_RE.match("src/libname"    ) is None


def _init_path_prefixes() -> typ.List[str]:
    py_path  = sys.executable.rsplit(os.sep, 2)[0]
    pwd      = os.getcwd()
    prefixes = {pwd, py_path}

    for path in sys.path:
        if py_match := PYTHON_ENV_RE.match(path):
            prefix = py_match.group('prefix')
            prefixes.add(prefix)

    # Strip the longer prefixes first. This ensures that
    # sub directories are stripped fully.
    return sorted((p.rstrip(os.sep) + os.sep for p in prefixes), key=len, reverse=True)


# Ordered by longest to shortest path
# [
#   ("env27_spkg", "/home/user/venv/lib/python2.7/site-packages"),
#   ("env27",      "/home/user/venv/lib/python2.7"),
#   ("pwd",        "/home/user/projects/project"),
#   ("home",       "/home/user"),
# ]


def _parse_sep(paths: typ.Iterable[str]) -> str:
    if any(":\\" in path for path in paths):
        return "\\"
    else:
        return "/"


def _by_prefix_len(candidate: typ.Tuple[Alias, Prefix]) -> int:
    return len(candidate[1])


def parse_aliases_prefixes(dir_paths: typ.Iterable[str]) -> AliasPrefixes:
    # NOTE (mb 2020-08-15): This does not use environment variables
    #   to detect $PWD or python paths. Instead everything is parsed,
    #   from the paths of the backtrace itself, regardless of context.
    #   This makes the formatting deterministic, regardless of the
    #   system on which it is run.

    # NOTE (mb 2020-08-15): This could be an endless rabbit hole,
    #   because it's an open question, what is a meaningful alias
    #   for any given path?
    #   To limit this, and make the output easier to understand,
    #   we have special casing for env/site-packages/dist-packages
    #   and other than that we just give each alias a number.
    sep = _parse_sep(dir_paths)

    longest_dir_paths = sorted(dir_paths, key=_by_prefix_len, reverse=True)

    alias_candidates: AliasPrefixes = []
    alias_count     : typ.Dict[Alias, int] = collections.defaultdict(int)

    for path in longest_dir_paths:
        # if sep == "/":
        #     is_pwd = not path.startswith("/")
        # else:
        #     is_pwd = WINPATH_RE.match(path) is None

        py_match   = PYTHON_ENV_RE.match(path)
        is_sitepkg = "site-packages" in path
        is_distpkg = "dist-packages" in path
        is_env     = py_match and "env" in path
        is_py      = py_match and not is_env

        if is_sitepkg:
            if alias_count['sitepkg'] == 0:
                alias = "sitepkg"
            else:
                alias = "sitepkg-" + alias_count['sitepkg']

            prefix = path.rsplit("site-packages", 1)[0] + "site-packages"
            alias_candidates.append((alias, prefix))
            alias_count['sitepkg'] += 1
        elif is_distpkg:
            if alias_count['distpkg'] == 0:
                alias = "distpkg"
            else:
                alias = "distpkg-" + alias_count['distpkg']

            prefix = path.rsplit("dist-packages", 1)[0] + "dist-packages"
            alias_candidates.append((alias, prefix))
            alias_count['distpkg'] += 1
        elif is_env:
            py_match
            prefix    = path.rsplit("env", 1)[0] + sep + "dist-packages"
            candidate = ("env", prefix)
            alias_candidates.append(candidate)
            alias_count['env'] += 1
        elif is_py:
            alias_count['py'] += 1

    return aliases


def parse_entry_aliase_prefixes(entries: typ.Sequence[com.Entry]) -> AliasPrefixes:
    sep = _parse_sep(e.module for e in entries)

    dir_paths = {e.module.rsplit(sep, 1)[0] for e in entries}
    return parse_aliases_prefixes(dir_paths)


def parse_prefixes(entries: typ.Sequence[com.Entry]) -> typ.List[str]:
    sep               = _parse_sep(e.module for e in entries)
    dir_paths         = [e.module.rsplit(sep, 1)[0] for e in entries]
    longest_dir_paths = sorted(set(dir_paths), key=len, reverse=True)

    # prefixes = []
    # print()
    # for path in longest_dir_paths:
    #     print(repr(path))

    # return []
    return [
        "/home/user/venv/lib/python2.7/site-packages",
        "/home/user/src/project-common/project_common",
        "/home/user/venv/lib/python2.7/",
        "/home/user/envs/py38/lib/python3.8/",
    ]


def _iter_entry_paths(entries: com.Entries) -> typ.Iterable[str]:
    for entry in entries:
        module_abspath   = os.path.abspath(entry.module)
        is_valid_abspath = module_abspath != entry.module and os.path.exists(module_abspath)
        if is_valid_abspath:
            yield module_abspath
        else:
            yield entry.module


def _init_aliases(entry_paths: typ.List[str]) -> AliasPrefixes:
    _uniq_entry_paths = set(entry_paths)

    paths = list(sys.path)
    paths.sort(key=len)

    pwd = os.getcwd()
    if pwd in paths:
        paths.remove(pwd)
    paths.append(pwd)

    alias_index = 0
    aliases: AliasPrefixes = []
    for path in reversed(paths):
        is_path_used = False
        for epath in _uniq_entry_paths:
            if epath.startswith(path):
                is_path_used = True
                _uniq_entry_paths.remove(epath)
                break

        if not is_path_used:
            continue

        if path.endswith("site-packages"):
            alias = "<sitepkg>"
        elif path == pwd:
            alias = "<pwd>"
        elif re.search(r"lib/python\d.\d+$", path):
            alias = "<py>"
        elif re.search(r"lib/Python\d.\d+\\lib$", path):
            alias = "<py>"
        else:
            alias = f"<p{alias_index}>"
            alias_index += 1

        aliases.append((alias, path))

    return aliases


def _init_entry_context(entries: com.Entries) -> Context:
    entry_paths = list(_iter_entry_paths(entries))
    aliases     = _init_aliases(entry_paths)

    rows: Rows = []

    for module, entry in zip(entry_paths, entries):
        _module, call, lineno, context = entry
        assert module.endswith(_module)

        used_alias   = ""
        module_short = module
        for alias, path in aliases:
            if module.startswith(path):
                used_alias   = alias
                module_short = module[len(path) :]
                break

        rows.append([used_alias, module_short, call, lineno, context])

    max_module_len = max(len(row[0]) + len(row[1]) for row in rows)
    max_lineno_len = max(len(row[3]) for row in rows)
    max_call_len   = max(len(row[2]) for row in rows)

    return Context(rows, aliases, max_module_len, max_lineno_len, max_call_len,)


def _update_padding(ctx: Context) -> None:
    # Expand padding from left to right as much as can fit the terminal.
    # This will mutate rows (updating strings with added padding)

    columns = _get_terminal_width()

    for row in ctx.rows:
        alias, module, call, lineno, context = row
        len_module = len(alias) + len(module)
        line_len   = 2 + len_module + 2 + len(call) + 2 + len(lineno) + 2 + len(context)

        padding_available = columns - line_len
        if padding_available <= 0:
            continue

        padding_desired  = ctx.max_module_len - len_module
        padding_consumed = min(padding_available, padding_desired)
        row[1] = module + " " * padding_consumed

        padding_available -= padding_consumed
        if padding_available <= 0:
            continue

        padding_desired  = ctx.max_call_len - len(call)
        padding_consumed = min(padding_available, padding_desired)
        row[2] = call.ljust(len(call) + padding_consumed)

        padding_available -= padding_consumed
        if padding_available <= 0:
            continue

        padding_desired  = ctx.max_lineno_len - len(lineno)
        padding_consumed = min(padding_available, padding_desired)
        row[3] = lineno.rjust(len(lineno) + padding_consumed)


def _rows_to_lines(ctx: Context, color: bool = False) -> typ.Iterable[str]:
    # apply colors and additional separators/ spacing
    fmt_module  = FMT_MODULE if color else "{0}"
    fmt_call    = FMT_CALL if color else "{0}"
    fmt_lineno  = FMT_LINENO if color else "{0}"
    fmt_context = FMT_CONTEXT if color else "{0}"

    if ctx.aliases:
        alias_padding = max(len(alias) for alias, _ in ctx.aliases)
        for alias, path in ctx.aliases:
            yield "    " + alias.ljust(alias_padding) + ": " + fmt_module.format(path)

        yield ""

    for alias, module, call, lineno, context in ctx.rows:
        parts = (
            "    ",
            alias,
            fmt_module.format(module),
            "  ",
            fmt_call.format(call),
            "  ",
            fmt_lineno.format(lineno),
            ": ",
            fmt_context.format(context),
        )
        yield "".join(parts)


def _traceback_to_entries(traceback: types.TracebackType) -> typ.Iterable[com.Entry]:
    summary = tb.extract_tb(traceback)
    for entry in summary:
        module  = entry[0]
        call    = entry[2]
        lineno  = str(entry[1])
        context = entry[3]
        yield com.Entry(module, call, lineno, context)


def format_traceback(traceback: com.Traceback, color: bool = False) -> str:
    fmt_error  = FMT_ERROR if color else "{0}"
    error_line = fmt_error.format(traceback.exc_name)
    if traceback.exc_msg:
        error_line += ": " + traceback.exc_msg

    ctx = _init_entry_context(traceback.entries)
    _update_padding(ctx)
    lines = [com.TRACEBACK_HEAD]
    lines.extend(_rows_to_lines(ctx, color))
    lines.append(error_line)
    return os.linesep.join(lines) + os.linesep


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


def exc_to_traceback_str(
    exc_value: BaseException, traceback: types.TracebackType, color: bool = False,
) -> str:
    # NOTE (mb 2020-08-13): wrt. cause vs context see
    #   https://www.python.org/dev/peps/pep-3134/#enhanced-reporting
    #   https://stackoverflow.com/questions/11235932/
    tracebacks: typ.List[com.Traceback] = []

    cur_exc_value: BaseException       = exc_value
    cur_traceback: types.TracebackType = traceback

    while cur_exc_value:
        next_cause   = getattr(cur_exc_value, '__cause__'  , None)
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
            cur_traceback = next_cause.__traceback__
        elif next_context:
            cur_exc_value = next_context
            cur_traceback = next_context.__traceback__
        else:
            break

    tracebacks = list(reversed(tracebacks))

    return format_tracebacks(tracebacks, color)
