# [Pretty Traceback][repo_ref]

Human readable stacktraces for Python.

Project/Repo:

[![MIT License][license_img]][license_ref]
[![Supported Python Versions][pyversions_img]][pyversions_ref]
[![PyCalVer 2020.1015][version_img]][version_ref]
[![PyPI Version][pypi_img]][pypi_ref]
[![PyPI Downloads][downloads_img]][downloads_ref]

Code Quality/CI:

[![GitHub Build Status][github_build_img]][github_build_ref]
[![GitLab Build Status][gitlab_build_img]][gitlab_build_ref]
[![Type Checked with mypy][mypy_img]][mypy_ref]
[![Code Coverage][codecov_img]][codecov_ref]
[![Code Style: sjfmt][style_img]][style_ref]


|                 Name                |        role       |  since  | until |
|-------------------------------------|-------------------|---------|-------|
| Manuel Barkhau (mbarkhau@gmail.com) | author/maintainer | 2020-08 | -     |


## Overview

Pretty Traceback groups together what belongs together, adds coloring and alignment. All of this makes it easier for you to see patterns and filter out the signal from the noise. This tabular format is best viewed in a wide terminal.

In other words, get this 😍

<div align="center">
<p align="center">
  <img alt="logo" src="https://github.com/mbarkhau/pretty-traceback/raw/master/example_tb4.png">
</p>
</div>

Instead of this 🤮

```
Traceback (most recent call last):
  File "test/test_formatting.py", line 199, in <module>
    main()
  File "test/test_formatting.py", line 190, in main
    run_pingpong()
  File "test/test_formatting.py", line 161, in run_pingpong
    sched3.run()
  File "/home/mbarkhau/miniconda3/envs/pretty-traceback_py38/lib/python3.8/sched.py", line 151, in run
    action(*argument, **kwargs)
  File "/home/mbarkhau/miniconda3/envs/pretty-traceback_py38/lib/python3.8/sched.py", line 151, in run
    action(*argument, **kwargs)
  File "/home/mbarkhau/miniconda3/envs/pretty-traceback_py38/lib/python3.8/sched.py", line 151, in run
    action(*argument, **kwargs)
  File "test/test_formatting.py", line 151, in _ping
    _pong(depth + 1)
  File "test/test_formatting.py", line 129, in _pong
    _ping(depth + 1)
  File "test/test_formatting.py", line 136, in _ping
    sp.check_output(["command_that", "doesnt", "exist"])
  File "/home/mbarkhau/miniconda3/envs/pretty-traceback_py38/lib/python3.8/subprocess.py", line 411, in check_output
    return run(*popenargs, stdout=PIPE, timeout=timeout, check=True,
  File "/home/mbarkhau/miniconda3/envs/pretty-traceback_py38/lib/python3.8/subprocess.py", line 489, in run
    with Popen(*popenargs, **kwargs) as process:
  File "/home/mbarkhau/miniconda3/envs/pretty-traceback_py38/lib/python3.8/subprocess.py", line 854, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
  File "/home/mbarkhau/miniconda3/envs/pretty-traceback_py38/lib/python3.8/subprocess.py", line 1702, in _execute_child
    raise child_exception_type(errno_num, err_msg, err_filename)
FileNotFoundError: [Errno 2] No such file or directory: 'command_that'
```

If your terminal is wide enough, the long paths preserved.

<div align="center">
<p align="center">
  <img alt="logo" src="https://github.com/mbarkhau/pretty-traceback/raw/master/example_tb5.png">
</p>
</div>


## Usage

Add the following to your `__main__.py` or the equivalent module which is your entry point.

```python
try:
    import pretty_traceback
    pretty_traceback.install()
except ImportError:
    pass    # no need to fail because of missing dev dependency
```

Please do not add this code e.g. to your `__init__.py` or any other module that your users may import. They may not want you to mess with how their tracebacks are printed.

If you do feel the overwhelming desire to import the `pretty_traceback` in code that others might import, consider using the `envvar` argument, which will cause the install function to effectively be a noop unless you set `ENABLE_PRETTY_TRACEBACK=1`.

```python
try:
    import pretty_traceback
    pretty_traceback.install(envvar='ENABLE_PRETTY_TRACEBACK')
except ImportError:
    pass    # no need to fail because of missing dev dependency
```

Note, that the hook is only installed if the existing hook is the default. Any existing hooks that were installed before the call of `pretty_traceback.install` will be left in place.


## LoggingFormatter

A `logging.Formatter` subclass is also available (e.g. for integration with `flask`).

```python
import os
from flask.logging import default_handler

try:
    if os.getenv('FLASK_DEBUG') == "1":
        import pretty_traceback
        default_handler.setFormatter(pretty_traceback.LoggingFormatter())
except ImportError:
    pass    # no need to fail because of missing dev dependency
```


## More Examples

<div align="center">
<p align="center">
  <img alt="logo" src="https://github.com/mbarkhau/pretty-traceback/raw/master/example_tb0.png">
</p>
</div>

<div align="center">
<p align="center">
  <img alt="logo" src="https://github.com/mbarkhau/pretty-traceback/raw/master/example_tb3.png">
</p>
</div>

<div align="center">
<p align="center">
  <img alt="logo" src="https://github.com/mbarkhau/pretty-traceback/raw/master/example_tb_wide.png">
</p>
</div>



## Alternatives

Pretty Traceback is heavily inspired by the backtrace module by nir0s.

- https://github.com/nir0s/backtrace
- https://github.com/onelivesleft/PrettyErrors
- https://github.com/willmcgugan/rich#tracebacks
- https://github.com/aroberge/friendly-traceback
- https://github.com/laurb9/rich-traceback
- https://github.com/staticshock/colored-traceback.py
- https://github.com/chillaranand/ptb

[repo_ref]: https://github.com/mbarkhau/pretty-traceback

[github_build_img]: https://github.com/mbarkhau/pretty-traceback/workflows/CI/badge.svg
[github_build_ref]: https://github.com/mbarkhau/pretty-traceback/actions?query=workflow%3ACI

[gitlab_build_img]: https://gitlab.com/mbarkhau/pretty-traceback/badges/master/pipeline.svg
[gitlab_build_ref]: https://gitlab.com/mbarkhau/pretty-traceback/pipelines

[codecov_img]: https://gitlab.com/mbarkhau/pretty-traceback/badges/master/coverage.svg
[codecov_ref]: https://mbarkhau.gitlab.io/pretty-traceback/cov

[license_img]: https://img.shields.io/badge/License-MIT-blue.svg
[license_ref]: https://gitlab.com/mbarkhau/pretty-traceback/blob/master/LICENSE

[mypy_img]: https://img.shields.io/badge/mypy-checked-green.svg
[mypy_ref]: https://mbarkhau.gitlab.io/pretty-traceback/mypycov

[style_img]: https://img.shields.io/badge/code%20style-%20sjfmt-f71.svg
[style_ref]: https://gitlab.com/mbarkhau/straitjacket/

[pypi_img]: https://img.shields.io/badge/PyPI-wheels-green.svg
[pypi_ref]: https://pypi.org/project/pretty-traceback/#files

[downloads_img]: https://pepy.tech/badge/pretty-traceback/month
[downloads_ref]: https://pepy.tech/project/pretty-traceback

[version_img]: https://img.shields.io/static/v1.svg?label=PyCalVer&message=2020.1015&color=blue
[version_ref]: https://pypi.org/project/pycalver/

[pyversions_img]: https://img.shields.io/pypi/pyversions/pretty-traceback.svg
[pyversions_ref]: https://pypi.python.org/pypi/pretty-traceback
