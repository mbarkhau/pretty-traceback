# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import sys
import time
import sched
import subprocess as sp

import test.fixtures
from pretty_traceback import parsing
from pretty_traceback import formatting

# TODO (mb 2020-08-10): better formatting for long chains of module switches

# TODO (mb 2020-08-13): We don't test for any particular formatting,
#   just that all parts of the traceback are in the formatted string,
#   and in the correct order.

TEST_PATHS_WIN = [
    "C:\\Python38\\python38.zip",
    "C:\\Python38\\DLLs",
    "C:\\Python38\\lib",
    "C:\\Python38",
    "C:\\Python38\\lib\\site-packages",
    "c:\\users\\user\\venv38",
    "c:\\users\\user\\venv38\\lib\\site-packages",
    "c:\\users\\user\\venv38\\lib\\site-packages\\IPython\\extensions",
    "C:\\Users\\user\\.ipython",
]

TEST_PATHS_UNIX = [
    "/home/user/.local/lib/python3.8/site-packages",
    "/home/user/miniconda3/envs/pretty-traceback_py38/lib/python3.8",
    "/home/user/miniconda3/envs/pretty-traceback_py38/lib/python3.8/lib-dynload",
    "/home/user/miniconda3/envs/pretty-traceback_py38/lib/python3.8/site-packages",
]


def test_python_env_pattern():
    for path in TEST_PATHS_UNIX + TEST_PATHS_WIN:
        match = formatting.PYTHON_ENV_RE.match(path)
        assert match, f"No match for {path}"

    path = "/home/user/projects/myproject/"
    assert formatting.PYTHON_ENV_RE.match(path) is None


VALID_ALIAS_PREFIXES = {
    ("sitepkg" , "/home/user/miniconda3/envs/pretty-traceback_py38/lib/python3.8/site-packages"),
    ("env"     , "/home/user/miniconda3/envs/pretty-traceback_py38/"),
    ("env/lib" , "/home/user/miniconda3/envs/pretty-traceback_py38/lib"),
    ("env/bin" , "/home/user/miniconda3/envs/pretty-traceback_py38/bin"),
    ("env"     , "/home/user/miniconda3/envs/pretty-traceback_py38/lib/python3.8"),
    ("py_dpkg" , "/usr/local/lib/python3.8/dist-packages"),
    ("sitepkg" , "/home/user/venv/lib/python2.7/site-packages"),
    ("env"     , "/home/user/venv/lib/python2.7"),
    ("pwd"     , "/home/user/projects/project"),
    ("env_spkg", "c:\\users\\user\\venv38\\lib\\site-packages"),
    ("py_spkg" , "C:\\Python38\\lib\\site-packages"),
    ("home"    , "C:\\Users\\user"),
    ("env"     , "C:\\Python38"),
}


def test_parse_aliases_prefixes():
    alias_prefixes = parse_aliases_prefixes(TEST_PATHS_UNIX)
    for alias, prefix in alias_prefixes:
        print(repr(alias).ljust(20), repr(prefix))
        # assert (alias, prefix) in VALID_ALIAS_PREFIXES

    alias_prefixes = parse_aliases_prefixes(TEST_PATHS_WIN)
    for alias, prefix in alias_prefixes:
        print(repr(alias).ljust(20), repr(prefix))
        # assert (alias, prefix) in VALID_ALIAS_PREFIXES


def test_formatting():
    for trace_str in test.fixtures.ALL_TRACEBACK_STRS:
        tracebacks = parsing.parse_tracebacks(trace_str)
        for traceback in tracebacks:
            tb_str   = formatting.format_traceback(traceback)
            tb_lines = tb_str.splitlines()
            assert traceback.exc_name in tb_lines[-1]
            assert traceback.exc_msg  in tb_lines[-1]
            entry_lines = [line for line in tb_lines if line.startswith("    ")]
            assert len(entry_lines) == len(traceback.entries)
            for line, entry in zip(entry_lines, traceback.entries):
                assert entry.lineno  in line
                assert entry.src_ctx in line
                assert entry.call    in line

            # TODO (mb 2020-08-15): make sure paths are in the lines
            # print("---", (line, entry.module.rsplit("/")[-1]))
            # assert entry.module.rsplit("/")[-1] in line


def _pong(depth):
    _ping(depth + 1)


def _ping(depth=0):
    if depth > 2:
        try:
            sp.check_output(["command_that", "doesnt", "exist"])
        except IOError:
            try:
                raise AttributeError()
            except AttributeError as attr_err:
                new_ex = KeyError("Wrapping KeyError")
                # NOTE (mb 2020-08-13): This is equivalent to the following python3 syntax
                # raise new_ex from attr_err
                _, exc_value, traceback = sys.exc_info()
                assert exc_value is attr_err
                new_ex.__cause__     = exc_value
                new_ex.__traceback__ = traceback
                raise new_ex

    _pong(depth + 1)


def run_pingpong():
    sched1 = sched.scheduler(time.time, time.sleep)
    sched1.enter(0.1, 1, _ping, ())
    sched2 = sched.scheduler(time.time, time.sleep)
    sched2.enter(0.1, 1, sched1.run, ())
    sched3 = sched.scheduler(time.time, time.sleep)
    sched3.enter(0.1, 1, sched2.run, ())
    sched3.run()


def test_pingpong():
    try:
        run_pingpong()
    except KeyError:
        exc_type, exc_value, traceback = sys.exc_info()
        assert exc_type == type(exc_value)
        tb_str = formatting.exc_to_traceback_str(exc_value, traceback, color=False)
        assert isinstance(tb_str, str)
        # TODO (mb 2020-08-14): compare to test.fixture.CHAINED_TRACEBACK


def main():
    trace_strs = test.fixtures.ALL_TRACEBACK_STRS[1:]
    # trace_strs = test.fixtures.ALL_TRACEBACK_STRS
    for trace_str in trace_strs:
        tracebacks = parsing.parse_tracebacks(trace_str)
        tb_str     = formatting.format_tracebacks(tracebacks, color=True)
        print(tb_str)
        print("\n------------------------------\n")

    return

    try:
        run_pingpong()
    except KeyError:
        _, exc_value, traceback = sys.exc_info()
        tb_str = formatting.exc_to_traceback_str(exc_value, traceback, color=True)
        print(tb_str)


if __name__ == '__main__':
    main()
