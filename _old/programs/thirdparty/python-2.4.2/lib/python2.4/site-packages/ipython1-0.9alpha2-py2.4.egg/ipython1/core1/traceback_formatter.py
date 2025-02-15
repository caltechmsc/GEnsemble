""" Some formatter objects to extract traceback information by replacing
sys.excepthook().
"""

# Standard library imports.
import traceback


class ITracebackFormatter(object):
    """ Objects conforming to this interface will format tracebacks into other
    objects.
    """

    # The kind of formatter.
    kind = 'traceback'

    # The unique identifier for this formatter.
    identifier = None


    def __call__(self, exc_type, exc_value, exc_traceback):
        """ Return a formatted representation of a traceback.
        """

        raise NotImplementedError


class PlainTracebackFormatter(ITracebackFormatter):
    """ Return a string with the regular traceback information.
    """

    # The unique identifier for this formatter.
    identifier = 'plain'


    def __init__(self, limit=None):
        # The maximum number of stack levels to go back.
        # None implies all stack levels are returned.
        self.limit = limit
    
    def __call__(self, exc_type, exc_value, exc_traceback):
        """ Return a string with the regular traceback information.
        """

        lines = traceback.format_tb(exc_traceback, self.limit)
        lines.append('%s: %s' % (exc_type.__name__, exc_value))
        return '\n'.join(lines)


