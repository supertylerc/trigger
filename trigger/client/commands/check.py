"""Check command for Trigger."""

from __future__ import unicode_literals, print_function
import os
import sys

from simpleparse.error import ParserSyntaxError
from twisted.python import log


from trigger.acl.parser import parse, TIP, Protocol, Comment
from trigger.acl.tools import check_access, create_trigger_term
from trigger.client.commands.base import Command


class Check(Command):
    """Class for running the check command."""

    def _setup(self):
        """Get check ready."""
        if os.getenv('TRIGGER_DEBUG') or self.options['--verbose']:
            log.startLogging(sys.stdout, setStdout=False)

    def _build_new_term(self):
        term = create_trigger_term(
            source_ips=self.source_address,
            dest_ips=self.destination_address,
            source_ports=[],
            dest_ports=self.destination_port,
            protocols=self.protocol,
            name='sr_____',
        )
        term.modifiers['count'] = 'sr_____'
        term.comments.append(Comment('check_access: ADD THIS TERM'))
        return term

    @property
    def source_address(self):
        """Source IP."""
        try:
            return [TIP(self.options['--source-address'])]
        except ValueError:
            return []

    @property
    def destination_address(self):
        """Destination IP."""
        try:
            return [TIP(self.options['--destination-address'])]
        except ValueError:
            return []

    @property
    def destination_port(self):
        """Destination port."""
        return [int(self.options['--destination-port'])]

    @property
    def protocol(self):
        """IP protocol."""
        try:
            return [Protocol(self.options['--protocol'])]
        except TypeError:
            return []

    def parse_acl(self):
        """Parse an ACL and return the ACL object."""
        try:
            with open(self.options['<file>']) as acl_fd:
                return parse(acl_fd.read())
        except ParserSyntaxError as err:
            err = str(err).split()
            sys.exit('Cannot parse {}:'.format(self.options['<file>']),
                     ' '.join(err[1:]))

    @property
    def access_is_permitted(self):
        """Determine if access is permitted."""
        acl = self.parse_acl()
        new_term = self._build_new_term()
        return check_access(acl.terms, new_term, self.options['--quiet'],
                            format=acl.format, acl_name=acl.name)

    def run(self):
        """Run the bang command."""
        self._setup()
        if not self.access_is_permitted:
            return 1
        return 0
