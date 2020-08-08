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

import pytest

import pretty_traceback

FIXTURE = """
Traceback (most recent call last):
  File "/home/user/venvs/py38/bin/myproject", line 12, in <module>
    sys.exit(cli())
  File "/home/user/venvs/py38/lib/python3.8/site-packages/click/core.py", line 829, in __call__
    return self.main(*args, **kwargs)
  File "/home/user/venvs/py38/lib/python3.8/site-packages/click/core.py", line 782, in main
    rv = self.invoke(ctx)
  File "/home/user/venvs/py38/lib/python3.8/site-packages/click/core.py", line 1259, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
  File "/home/user/venvs/py38/lib/python3.8/site-packages/click/core.py", line 1066, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "/home/user/venvs/py38/lib/python3.8/site-packages/click/core.py", line 610, in invoke
    return callback(*args, **kwargs)
  File "/home/user/foss/myproject/src/myproject/cli.py", line 148, in build
    lp_gen_docs.gen_html(built_ctx, html_dir)
  File "/home/user/foss/myproject/src/myproject/gen_docs.py", line 295, in gen_html
    wrapped_html = wrap_content_html(content_html, 'screen', meta, toc)
  File "/home/user/foss/myproject/src/myproject/gen_docs.py", line 238, in wrap_content_html
    result = tmpl.render(**ctx)
  File "/home/user/venvs/py38/lib/python3.8/site-packages/jinja2/environment.py", line 1090, in render
    self.environment.handle_exception()
  File "/home/user/venvs/py38/lib/python3.8/site-packages/jinja2/environment.py", line 832, in handle_exception
    reraise(*rewrite_traceback_stack(source=source))
  File "/home/user/venvs/py38/lib/python3.8/site-packages/jinja2/_compat.py", line 28, in reraise
    raise value.with_traceback(tb)
  File "<template>", line 56, in top-level template code
TypeError: no loader for this environment specified
"""


def test_dummy():
    pass


# @pytest.fixture
# def captrace():
#     hook = pretty_traceback.init_excepthook(color=False)
#     hook_wrapper
#     sys.excepthook = hook_wrapper
#     yield


# def _pong(depth):
#     _ping(depth + 1)


# def _ping(depth=0):
#     if depth > 2:
#         try:
#             sp.check_output(["command_that", "doesnt", "exist"])
#         except Exception as ex:
#             new_ex = Exception("Wrapping Exception")
#             new_ex.__cause__ = ex
#             raise new_ex

#     _pong(depth + 1)


# def test_pingpong(captrace):
#     sched1 = sched.scheduler(time.time, time.sleep)
#     sched1.enter(0.1, 1, _ping, ())
#     sched2 = sched.scheduler(time.time, time.sleep)
#     sched2.enter(0.1, 1, sched1.run, ())
#     sched3 = sched.scheduler(time.time, time.sleep)
#     sched3.enter(0.1, 1, sched2.run, ())
#     sched3.run()
