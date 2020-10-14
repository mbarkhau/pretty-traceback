# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pretty_traceback.common as com

BASIC_TRACEBACK_STR = """
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
  File "/home/user/venvs/py38/lib/python3.8/site-packages/jinja2/environment.py", line 832, in handle_exce
    reraise(*rewrite_traceback_stack(source=source))
  File "/home/user/venvs/py38/lib/python3.8/site-packages/jinja2/_compat.py", line 28, in reraise
    raise value.with_traceback(tb)
  File "<template>", line 56, in top-level template code
TypeError: no loader for this environment specified
"""


BASIC_TRACEBACK_ENTRIES = [
    com.Entry(
        module="/home/user/venvs/py38/bin/myproject",
        call="<module>",
        lineno="12",
        src_ctx="sys.exit(cli())",
    ),
    com.Entry(
        module="/home/user/venvs/py38/lib/python3.8/site-packages/click/core.py",
        call="__call__",
        lineno="829",
        src_ctx="return self.main(*args, **kwargs)",
    ),
    com.Entry(
        module="/home/user/venvs/py38/lib/python3.8/site-packages/click/core.py",
        call="main",
        lineno="782",
        src_ctx="rv = self.invoke(ctx)",
    ),
    com.Entry(
        module="/home/user/venvs/py38/lib/python3.8/site-packages/click/core.py",
        call="invoke",
        lineno="1259",
        src_ctx="return _process_result(sub_ctx.command.invoke(sub_ctx))",
    ),
    com.Entry(
        module="/home/user/venvs/py38/lib/python3.8/site-packages/click/core.py",
        call="invoke",
        lineno="1066",
        src_ctx="return ctx.invoke(self.callback, **ctx.params)",
    ),
    com.Entry(
        module="/home/user/venvs/py38/lib/python3.8/site-packages/click/core.py",
        call="invoke",
        lineno="610",
        src_ctx="return callback(*args, **kwargs)",
    ),
    com.Entry(
        module="/home/user/foss/myproject/src/myproject/cli.py",
        call="build",
        lineno="148",
        src_ctx="lp_gen_docs.gen_html(built_ctx, html_dir)",
    ),
    com.Entry(
        module="/home/user/foss/myproject/src/myproject/gen_docs.py",
        call="gen_html",
        lineno="295",
        src_ctx="wrapped_html = wrap_content_html(content_html, 'screen', meta, toc)",
    ),
    com.Entry(
        module="/home/user/foss/myproject/src/myproject/gen_docs.py",
        call="wrap_content_html",
        lineno="238",
        src_ctx="result = tmpl.render(**ctx)",
    ),
    com.Entry(
        module="/home/user/venvs/py38/lib/python3.8/site-packages/jinja2/environment.py",
        call="render",
        lineno="1090",
        src_ctx="self.environment.handle_exception()",
    ),
    com.Entry(
        module="/home/user/venvs/py38/lib/python3.8/site-packages/jinja2/environment.py",
        call="handle_exce",
        lineno="832",
        src_ctx="reraise(*rewrite_traceback_stack(source=source))",
    ),
    com.Entry(
        module="/home/user/venvs/py38/lib/python3.8/site-packages/jinja2/_compat.py",
        call="reraise",
        lineno="28",
        src_ctx="raise value.with_traceback(tb)",
    ),
    com.Entry(
        module="<template>",
        call="top-level template code",
        lineno="56",
        src_ctx="",
    ),
]


BASIC_TRACEBACK = com.Traceback(
    exc_name="TypeError",
    exc_msg="no loader for this environment specified",
    entries=BASIC_TRACEBACK_ENTRIES,
    is_caused=False,
    is_context=False,
)


COMPRESSABLE_TRACEBACK_STR = """
Traceback (most recent call last):
  File "/home/user/venv/lib/python2.7/runpy.py", line 174, in _run_module_as_main
    "__main__", fname, loader, pkg_name)
  File "/home/user/venv/lib/python2.7/runpy.py", line 72, in _run_code
    exec code in run_globals
  File "/home/user/project/serve.py", line 19, in <module>
    import lib.http_util as http
  File "/home/user/venv/lib/python2.7/site-packages/gevent/builtins.py", line 93, in __import__
    result = _import(*args, **kwargs)
  File "/home/user/project/lib/http_util.py", line 27, in <module>
    import api.plugins
  File "/home/user/venv/lib/python2.7/site-packages/gevent/builtins.py", line 93, in __import__
    result = _import(*args, **kwargs)
  File "/home/user/project/api/plugins/__init__.py", line 21, in <module>
    from api.query import iter_doc_metrics
  File "/home/user/venv/lib/python2.7/site-packages/gevent/builtins.py", line 93, in __import__
    result = _import(*args, **kwargs)
  File "/home/user/project/api/query.py", line 25, in <module>
    import submodule
  File "/home/user/venv/lib/python2.7/site-packages/gevent/builtins.py", line 93, in __import__
    result = _import(*args, **kwargs)
  File "/home/user/project/submodule/__init__.py", line 7, in <module>
    import submodule.cell_calc as cell_calc    # noqa
  File "/home/user/venv/lib/python2.7/site-packages/gevent/builtins.py", line 93, in __import__
    result = _import(*args, **kwargs)
  File "/home/user/project/submodule/cell_calc.py", line 17, in <module>
    import submodule.constants as const
  File "/home/user/venv/lib/python2.7/site-packages/gevent/builtins.py", line 93, in __import__
    result = _import(*args, **kwargs)
  File "/home/user/project/submodule/constants.py", line 23, in <module>
    for preview_id, preview_cfg in cfg.__init__.BASE_CONFIG.val['preview_config'].items()
  File "/home/user/src/project-common/project_common/lib.py", line 102, in val
    return self.fresh_val
  File "/home/user/src/project-common/project_common/lib.py", line 77, in fresh_val
    self._res = self._process_func(_res)
  File "/home/user/project/cfg/__init__.py", line 1844, in _parse_base_config
    _update_dimension_defs(base_cfg)
  File "/home/user/project/cfg/__init__.py", line 476, in _update_dimension_defs
    _parse_dimension_formula(dim_def, all_dim_ids)
  File "/home/user/project/cfg/__init__.py", line 427, in _parse_dimension_formula
    assert hasattr(api.plugins.common, parse_fn_name), msg
AttributeError: 'module' object has no attribute 'plugins'
"""


CHAINED_TRACEBACK_STR = """
Traceback (most recent call last):
  File "./test/test_formatting.py", line 30, in _ping
    sp.check_output(['command_that', 'doesnt', 'exist'])
  File "/home/user/envs/py38/lib/python3.8/subprocess.py", line 411, in check_output
    return run(*popenargs, stdout=PIPE, timeout=timeout, check=True,
  File "/home/user/envs/py38/lib/python3.8/subprocess.py", line 489, in run
    with Popen(*popenargs, **kwargs) as process:
  File "/home/user/envs/py38/lib/python3.8/subprocess.py", line 854, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
  File "/home/user/envs/py38/lib/python3.8/subprocess.py", line 1702, in _execute_child
    raise child_exception_type(errno_num, err_msg, err_filename)
FileNotFoundError: [Errno 2] No such file or directory: 'command_that'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/user/project/test/test_formatting.py", line 35, in _ping
    raise AttributeError()
AttributeError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/user/project/test/test_formatting.py", line 70, in <module>
    run_pingpong()
  File "/home/user/project/test/test_formatting.py", line 56, in run_pingpong
    sched3.run()
  File "/home/user/envs/py38/lib/python3.8/sched.py", line 151, in run
    action(*argument, **kwargs)
  File "/home/user/envs/py38/lib/python3.8/sched.py", line 151, in run
    action(*argument, **kwargs)
  File "/home/user/envs/py38/lib/python3.8/sched.py", line 151, in run
    action(*argument, **kwargs)
  File "/home/user/project/test/test_formatting.py", line 46, in _ping
    _pong(depth + 1)
  File "/home/user/project/test/test_formatting.py", line 24, in _pong
    _ping(depth + 1)
  File "/home/user/project/test/test_formatting.py", line 42, in _ping
    raise new_ex
  File "/home/user/project/test/test_formatting.py", line 33, in _ping
    raise AttributeError()
KeyError: Wrapping KeyError
"""


CHAINED_TRACEBACK_ENTRIES_0 = [
    com.Entry(
        module="./test/test_formatting.py",
        call="_ping",
        lineno="30",
        src_ctx="sp.check_output(['command_that', 'doesnt', 'exist'])",
    ),
    com.Entry(
        module="/home/user/envs/py38/lib/python3.8/subprocess.py",
        call="check_output",
        lineno="411",
        src_ctx="return run(*popenargs, stdout=PIPE, timeout=timeout, check=True,",
    ),
    com.Entry(
        module="/home/user/envs/py38/lib/python3.8/subprocess.py",
        call="run",
        lineno="489",
        src_ctx="with Popen(*popenargs, **kwargs) as process:",
    ),
    com.Entry(
        module="/home/user/envs/py38/lib/python3.8/subprocess.py",
        call="__init__",
        lineno="854",
        src_ctx="self._execute_child(args, executable, preexec_fn, close_fds,",
    ),
    com.Entry(
        module="/home/user/envs/py38/lib/python3.8/subprocess.py",
        call="_execute_child",
        lineno="1702",
        src_ctx="raise child_exception_type(errno_num, err_msg, err_filename)",
    ),
]


CHAINED_TRACEBACK_ENTRIES_1 = [
    com.Entry(
        module="/home/user/project/test/test_formatting.py",
        call="_ping",
        lineno="35",
        src_ctx="raise AttributeError()",
    ),
]


CHAINED_TRACEBACK_ENTRIES_2 = [
    com.Entry(
        module="/home/user/project/test/test_formatting.py",
        call="<module>",
        lineno="70",
        src_ctx="run_pingpong()",
    ),
    com.Entry(
        module="/home/user/project/test/test_formatting.py",
        call="run_pingpong",
        lineno="56",
        src_ctx="sched3.run()",
    ),
    com.Entry(
        module="/home/user/envs/py38/lib/python3.8/sched.py",
        call="run",
        lineno="151",
        src_ctx="action(*argument, **kwargs)",
    ),
    com.Entry(
        module="/home/user/envs/py38/lib/python3.8/sched.py",
        call="run",
        lineno="151",
        src_ctx="action(*argument, **kwargs)",
    ),
    com.Entry(
        module="/home/user/envs/py38/lib/python3.8/sched.py",
        call="run",
        lineno="151",
        src_ctx="action(*argument, **kwargs)",
    ),
    com.Entry(
        module="/home/user/project/test/test_formatting.py",
        call="_ping",
        lineno="46",
        src_ctx="_pong(depth + 1)",
    ),
    com.Entry(
        module="/home/user/project/test/test_formatting.py",
        call="_pong",
        lineno="24",
        src_ctx="_ping(depth + 1)",
    ),
    com.Entry(
        module="/home/user/project/test/test_formatting.py",
        call="_ping",
        lineno="42",
        src_ctx="raise new_ex",
    ),
    com.Entry(
        module="/home/user/project/test/test_formatting.py",
        call="_ping",
        lineno="33",
        src_ctx="raise AttributeError()",
    ),
]


CHAINED_TRACEBACK = [
    com.Traceback(
        exc_name="FileNotFoundError",
        exc_msg="[Errno 2] No such file or directory: 'command_that'",
        entries=CHAINED_TRACEBACK_ENTRIES_0,
        is_caused=False,
        is_context=False,
    ),
    com.Traceback(
        exc_name="AttributeError",
        exc_msg="",
        entries=CHAINED_TRACEBACK_ENTRIES_1,
        is_caused=False,
        is_context=True,
    ),
    com.Traceback(
        exc_name="KeyError",
        exc_msg="Wrapping KeyError",
        entries=CHAINED_TRACEBACK_ENTRIES_2,
        is_caused=True,
        is_context=False,
    ),
]


ALL_TRACEBACK_STRS = [
    BASIC_TRACEBACK_STR,
    COMPRESSABLE_TRACEBACK_STR,
    CHAINED_TRACEBACK_STR,
]
