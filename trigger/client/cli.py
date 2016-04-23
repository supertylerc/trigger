# pylint: disable=line-too-long
r"""Trigger CLI.

trigger

Usage:
    trigger [options]
    trigger bang [-v | --verbose] [-o | --oob] <device>
    trigger check acl [-q | --quiet] [-v | --verbose] --source-address=<src_addr> --destination-address=<dest_addr> [--destination-port=<dest_port>] [--protocol=<proto>] <file>

Options:
    -h --help                          Show this help.
    -V --version                       Print the version of the Trigger client.
    -v --verbose                       Verbose output/logging.

Commands:
    bang       Connect to a network device.
    check acl  Check if an IP header tuple is permitted through an ACL.

bang Options:
    -o --oob                           Connect via the OOB device.

Examples:
    trigger bang core1-sfo.example.com
    trigger check acl --source-address=10.10.10.10\
        --destination-address=20.20.20.20\
        --destination-port=22\
        --protocol=tcp

Help:
    For additional help, open an issue on the project's GitHub project:
    https://github.com/trigger/trigger
"""  # noqa
# pylint: enable=line-too-long

from __future__ import unicode_literals, print_function
from inspect import getmembers, isclass
import sys

from docopt import docopt

from trigger import __version__ as VERSION


def main():
    """Entrypoint."""
    from trigger.client import commands
    options = docopt(__doc__, version=VERSION)
    for key in options:
        if not options[key]:
            continue
        if hasattr(commands, key):
            module = getattr(commands, key)
            commands = getmembers(module, isclass)
            command = [cmd[1] for cmd in commands if cmd[0] != 'Command'][0]
            command = command(options)
            sys.exit(command.run())
