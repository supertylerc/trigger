"""Base class for Trigger commands."""

from __future__ import unicode_literals


# pylint: disable=too-few-public-methods
class Command(object):
    """Base command class."""

    def __init__(self, options, *args, **kwargs):
        """Create a new Command."""
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """Run the command."""
        raise NotImplementedError('Subclass must implement run.')
# pylint: enable=too-few-public-methods
