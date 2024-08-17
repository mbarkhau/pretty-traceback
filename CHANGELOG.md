# Changelog for https://github.com/mbarkhau/pretty-traceback

## 2024.1021

- Update: Avoid leading / on relative paths. [gh#13][gh13]

[gh13]: https://github.com/mbarkhau/pretty-traceback/pull/13


## 2023.1020

- Fix: Prevent errors in non-tty environments [gh#9][gh9]

[gh9]: https://github.com/mbarkhau/pretty-traceback/issues/9


## 2023.1019

- Update: Append lineno to filename so it can be parsed by editors/IDEs. [gh#8][gh8]

[gh8]: https://github.com/mbarkhau/pretty-traceback/pull/8


## 2022.1018

- Add final newline to output. See [gh#3][gh3]

[gh3]: https://github.com/mbarkhau/pretty-traceback/issues/3


## 2021.1017

- Fix highlight in wide mode


## 2020.1016

- Shorten tracebacks for `RecursionError`


## 2020.1012

- Improve alias selection


## 2020.1011

- Fix github #1: Invalid path handling for `./script.py`


## 2020.1010

- Fix gitlab #5: Only show aliases that were actually used.
- Fix gitlab #5: Better alignment on narrow terminals.


## 2020.1009

- Fix gitlab #3: Corner case where exception has `None` as context.
- Fix gitlab #2: Improve formatting when line overflows.


## 2020.1008

- Add `pretty_traceback.LoggingFormatter`


## 2020.1006

- Add wide mode.


## 2020.1005

- Update formatting to work better with recursive calls.
- Add tests


## 2020.1001

- Initial release
