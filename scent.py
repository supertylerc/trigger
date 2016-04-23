"""Custom Sniffer runner."""

import os
from subprocess import call
from sniffer.api import file_validator, runnable


watch_paths = ['./trigger_client/', './tests/']

@file_validator
def py_files(filename):
    """Only run for files ending in `.py`, but not starting with `.`."""
    return (filename.endswith('.py')
            and not os.path.basename(filename).startswith('.'))


@runnable
def make_test(*_):
    """Run `make test`."""
    return call('make test', shell=True) == 0
