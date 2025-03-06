from . import formatting
import pytest

def pytest_addini(parser):
    parser.addini(
        "enable_pretty_traceback",
        "Enable the pretty traceback plugin",
        type="bool",
        default=True
    )

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest stack traces are challenging to work with by default. This plugin allows pretty_traceback to be used instead.

    This little piece of code was hard-won:

    https://grok.com/share/bGVnYWN5_951be3b1-6811-4fda-b220-c1dd72dedc31
    """
    outcome = yield
    report = outcome.get_result()  # Get the generated TestReport object

    # Check if the report is for the 'call' phase (test execution) and if it failed
    if item.config.getini("enable_pretty_traceback") and report.when == "call" and report.failed:
        value = call.excinfo.value
        tb = call.excinfo.tb
        formatted_traceback = formatting.exc_to_traceback_str(value, tb, color=True)
        report.longrepr = formatted_traceback