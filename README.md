# [Pretty Traceback][repo_ref]

Human readable stacktraces for Python.

Project/Repo:

[![MIT License][license_img]][license_ref]
[![Supported Python Versions][pyversions_img]][pyversions_ref]
[![PyCalVer 2020.1010][version_img]][version_ref]
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
  <img alt="logo" src="https://github.com/mbarkhau/pretty-traceback/raw/master/example_tb3.png">
</p>
</div>

Instead of this 🤮

```
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
```

If you're terminal is not wide enough, the long paths are replaced with aliases.

<div align="center">
<p align="center">
  <img alt="logo" src="https://github.com/mbarkhau/pretty-traceback/raw/master/example_tb2.png">
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
  <img alt="logo" src="https://github.com/mbarkhau/pretty-traceback/raw/master/example_tb1.png">
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

[version_img]: https://img.shields.io/static/v1.svg?label=PyCalVer&message=2020.1010&color=blue
[version_ref]: https://pypi.org/project/pycalver/

[pyversions_img]: https://img.shields.io/pypi/pyversions/pretty-traceback.svg
[pyversions_ref]: https://pypi.python.org/pypi/pretty-traceback
