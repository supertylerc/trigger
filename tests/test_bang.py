"""Test trigger bang."""

from unittest import TestCase
from collections import namedtuple

from mock import patch

import trigger
import trigger.netdevices
import os

class TestBang(TestCase):
    def setUp(self):
        self.opts = {
            '<device>': '1.2.3.4',
            '--oob': False,
            '--verbose': False
        }
        NetDevice = namedtuple('NetDevice',
            'adminStatus, nodeName, '
            'manufacturer, connect, OOBTerminalServerFQDN, '
            'OOBTerminalServerTCPPort')
        with patch.object(trigger.netdevices, 'device_match') as m:
            m.return_value = NetDevice(
                adminStatus='PRODUCTION',
                nodeName='1.2.3.4',
                manufacturer='JUNIPER',
                OOBTerminalServerFQDN='1.2.3.5',
                OOBTerminalServerTCPPort=7023,
                connect=lambda: 0
            )
            # Annoying requirement to import `Bang` after the mock,
            # otherwise the mock doesn't take effect.
            from trigger.client.commands.bang import Bang
            self.bang = Bang(self.opts)
            self.bang._setup()

    def test_connect(self):
        self.assertEqual(0, self.bang.connect())

    def test_connect_via_oob(self):
        with patch.object(os, 'system') as m:
            m.return_value = 0
            self.assertEqual(0, self.bang.connect_via_oob())

    def test__dispatch_no_device(self):
        self.bang.device = None
        self.assertEqual(2, self.bang._dispatch())

    def test_run(self):
        self.assertEqual(0, self.bang.run())
