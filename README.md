# [Pretty Traceback][repo_ref]

Human readable stacktraces for Python.

Project/Repo:

[![MIT License][license_img]][license_ref]
[![Supported Python Versions][pyversions_img]][pyversions_ref]
[![PyCalVer 2020.1003][version_img]][version_ref]
[![PyPI Version][pypi_img]][pypi_ref]
[![PyPI Downloads][downloads_img]][downloads_ref]

Code Quality/CI:

[![Build Status][build_img]][build_ref]
[![Type Checked with mypy][mypy_img]][mypy_ref]
[![Code Coverage][codecov_img]][codecov_ref]
[![Code Style: sjfmt][style_img]][style_ref]


|                 Name                |        role       |  since  | until |
|-------------------------------------|-------------------|---------|-------|
| Manuel Barkhau (mbarkhau@gmail.com) | author/maintainer | 2020-08 | -     |


## Overview

Pretty Traceback groups together what belongs together, rather than showing each part of the traceback as if they were all an equally likely source of a bug. This grouping lets you see, what code relates to frameworks or libraries and what code belong to **your project**, which is of course much more likely to be where the **root cause** of the issue is.

In other words, get this 😍

<!-- TODO: replace with svg, because colouring in Markdown does not reflect output on the terminal. -->

```python
/home/user/venvs/py38/bin/myproject
                             <module>                  12: sys.exit(cli())

/home/user/venvs/py38/lib/python3.8/site-packages/
  click/core.py  __call__  829: return self.main(*args, **kwargs)
  click/core.py  main      782: rv = self.invoke(ctx)
  click/core.py  invoke   1259: return _process_result(sub_ctx.command.invoke(sub_ctx))
  click/core.py  invoke   1066: return ctx.invoke(self.callback, **ctx.params)
  click/core.py  invoke    610: return callback(*args, **kwargs)

/home/user/foss/myproject/src/myproject/
  src/myproject/cli.py       build              160: lp_gen_docs.gen_html(built_ctx, html_dir)
  src/myproject/gen_docs.py  gen_html           294: wrapped_html = wrap_content_html(content_html, 'screen', meta, toc)
  src/myproject/gen_docs.py  wrap_content_html  237: result = tmpl.render(**ctx)

/home/user/venvs/py38/lib/python3.8/site-packages/
  jinja2/environment.py  render            1090: self.environment.handle_exception()
  jinja2/environment.py  handle_exception   832: reraise(*rewrite_traceback_stack(source=source))
  jinja2/_compat.py      reraise             28: raise value.with_traceback(tb)

<template>                   top-level template code   56:

TypeError: no loader for this environment specified
```

Instead of this 🤮

```python
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


## Alternatives

Pretty Traceback is heavilly inspired by the backtrace modile by nir0s.

- https://github.com/nir0s/backtrace
- https://github.com/willmcgugan/rich#tracebacks
- https://github.com/aroberge/friendly-traceback
- https://github.com/laurb9/rich-traceback
- https://github.com/staticshock/colored-traceback.py
- https://github.com/chillaranand/ptb

[repo_ref]: https://gitlab.com/mbarkhau/pretty-traceback

[build_img]: https://gitlab.com/mbarkhau/pretty-traceback/badges/master/pipeline.svg
[build_ref]: https://gitlab.com/mbarkhau/pretty-traceback/pipelines

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

[version_img]: https://img.shields.io/static/v1.svg?label=PyCalVer&message=2020.1003&color=blue
[version_ref]: https://pypi.org/project/pycalver/

[pyversions_img]: https://img.shields.io/pypi/pyversions/pretty-traceback.svg
[pyversions_ref]: https://pypi.python.org/pypi/pretty-traceback
