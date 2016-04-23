"""Bang command for Trigger."""

from __future__ import unicode_literals, print_function
import os
import sys

from twisted.python import log

from trigger.netdevices import device_match
from trigger.client.commands.base import Command


class Bang(Command):
    """Class for running the bang command."""

    device = None

    def _setup(self):
        """Get bang ready."""
        if os.getenv('TRIGGER_DEBUG') or self.options['--verbose']:
            log.startLogging(sys.stdout, setStdout=False)
        self.device = device_match(self.options['<device>'],
                                   production_only=False)

    def _dispatch(self):
        """Dispatch to the right connection method."""
        if self.device is None:
            return 2
        if self.device.adminStatus != 'PRODUCTION':
            print('WARNING: You are connecting to a non-production device.')
        if self.options['--oob']:
            return self.connect_via_oob()
        return self.connect()

    def connect_via_oob(self):
        """Connect to a device via its OOB device."""
        telnet = 'telnet {} {}'.format(self.device.OOBTerminalServerFQDN,
                                       self.device.OOBTerminalServerTCPPort)

        print('OOB Information for {}:'.format(self.device.nodeName))
        print(telnet)
        print('Connecting you now...')
        return os.system(telnet)

    def connect(self):
        """Connect directly to a device."""
        return self.device.connect()

    def run(self):
        """Run the bang command."""
        self._setup()
        return self._dispatch()
