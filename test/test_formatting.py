# pylint: disable=redefined-outer-name
# pylint: disable=protected-access
# pylint: disable=unused-argument

import os
import re
import sys
import time
import sched
import random
import subprocess as sp

import builtins

import test.fixtures

import pytest

from pretty_traceback2 import common
from pretty_traceback2 import parsing
from pretty_traceback2 import formatting

text_type = getattr(builtins, "unicode", str)


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
    "/home/user/project",
    "/home/user/foss/myproject",
    # "/home/user/venvs/py38/bin",
    "/home/user/src/project-common",
    "/home/user/venv/lib/python2.7",
    "/home/user/envs/py38/lib/python3.8",
    "/home/user/venv/lib/python2.7/site-packages",
    "/home/user/.local/lib/python3.8/site-packages",
    "/home/user/venvs/py38/lib/python3.8/site-packages",
    "/home/user/venvs/py38",
    "/home/user/foss/myproject/src/myproject",
]


@pytest.fixture
def env_setup():
    formatting.TEST_PATHS = TEST_PATHS_WIN + TEST_PATHS_UNIX
    formatting.PWD = "/home/user/foss/myproject"
    yield
    del formatting.TEST_PATHS[:]
    formatting.PWD = os.getcwd()


def test_formatting_basic():
    for trace_str in test.fixtures.ALL_TRACEBACK_STRS:
        tracebacks = parsing.parse_tracebacks(trace_str)
        for traceback in tracebacks:
            tb_str = formatting.format_traceback(traceback)
            tb_entries_str = tb_str.split(common.TRACEBACK_HEAD)[-1]
            tb_entry_lines = tb_entries_str.splitlines()
            assert traceback.exc_name in tb_entry_lines[-1]
            assert traceback.exc_msg in tb_entry_lines[-1]
            entry_lines = [line for line in tb_entry_lines if line.startswith("    ")]
            assert len(entry_lines) == len(traceback.entries)
            for line, entry in zip(entry_lines, traceback.entries):
                assert entry.lineno in line
                assert entry.src_ctx in line
                assert entry.call in line

                fname = entry.module.rsplit("/")[-1].rsplit("\\")[-1]
                assert fname in line


FORMATTING_TEST_CASES = [
    (0, 10, r"    \<\w+\>.*\.py:\d+[ ]+"),
    (1, 10, r"    \<\w+\>.*\.py:\d+[ ]+"),
    (0, 1000, r"    .*\.py:\d+[ ]+"),
    (1, 1000, r"    .*\.py:\d+[ ]+"),
]


@pytest.mark.parametrize("fixture_index, term_width, pathsep_re", FORMATTING_TEST_CASES)
def test_formatting(fixture_index, term_width, pathsep_re, env_setup):
    trace_str = test.fixtures.ALL_TRACEBACK_STRS[fixture_index]
    for traceback in parsing.parse_tracebacks(trace_str):
        ctx = formatting._init_entries_context(traceback.entries, term_width=term_width)
        tb_str = formatting._format_traceback(ctx, traceback)

        pathsep_offsets = []

        tb_lines = tb_str.split(common.TRACEBACK_HEAD)[-1].strip(os.linesep).splitlines()[:-1]
        for line in tb_lines:
            assert line.startswith("    "), repr(line)

            pathsep_match = re.search(pathsep_re, line)
            if pathsep_match:
                _, end = pathsep_match.span()
                pathsep_offsets.append(end)

        # all line numbers are aligned to the right at the same offset
        assert len(pathsep_offsets) > 3 and len(set(pathsep_offsets)) == 1


def _pong(depth):
    _ping(depth + 1)


def _ping(depth=0):
    # pylint:disable=raise-missing-from  ; that's the point of the test...
    if depth > 1:
        try:
            sp.check_output(["command_that", "doesnt", "exist"])
        except (OSError, IOError):
            try:
                raise AttributeError()
            except AttributeError as attr_err:
                new_ex = KeyError("Wrapping KeyError")
                # NOTE (mb 2020-08-13): This is equivalent to the following python3 syntax
                # raise new_ex from attr_err
                _, exc_value, traceback = sys.exc_info()
                assert exc_value is attr_err
                new_ex.__cause__ = exc_value
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
        assert exc_type is type(exc_value)
        tb_str = formatting.exc_to_traceback_str(exc_value, traceback, color=False)
        assert isinstance(tb_str, text_type)
        # TODO (mb 2020-08-14): compare to test.fixture.CHAINED_TRACEBACK


def run_max_recursion():
    def _mutual_recurse_a():
        if random.random() > 0.5:
            _mutual_recurse_b()
        else:
            _mutual_recurse_c()

    def _mutual_recurse_b():
        if random.random() > 0.5:
            _mutual_recurse_a()
        else:
            _mutual_recurse_c()

    def _mutual_recurse_c():
        if random.random() > 0.5:
            _mutual_recurse_a()
        else:
            _mutual_recurse_b()

    try:
        _mutual_recurse_a()
    except RecursionError:
        _exc_type, exc_value, traceback = sys.exc_info()
        tb_str = formatting.exc_to_traceback_str(exc_value, traceback, color=True)
        print(tb_str)


def main():
    run_max_recursion()

    formatting.PWD = "/home/user/foss/myproject"
    formatting.TEST_PATHS = TEST_PATHS_WIN + TEST_PATHS_UNIX
    trace_strs = test.fixtures.ALL_TRACEBACK_STRS

    for trace_str in trace_strs:
        tracebacks = parsing.parse_tracebacks(trace_str)
        tb_str = formatting.format_tracebacks(tracebacks, color=True)
        print(tb_str)
        print("\n------------------------------\n")

    formatting.PWD = os.getcwd()
    del formatting.TEST_PATHS[:]

    try:
        run_pingpong()
    except KeyError:
        _, exc_value, traceback = sys.exc_info()
        tb_str = formatting.exc_to_traceback_str(exc_value, traceback, color=True)
        print(tb_str)


if __name__ == "__main__":
    main()
