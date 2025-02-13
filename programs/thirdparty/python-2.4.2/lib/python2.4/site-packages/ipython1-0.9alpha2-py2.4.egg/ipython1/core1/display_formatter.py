""" Objects for replacing sys.displayhook().
"""


class IDisplayFormatter(object):
    """ Objects conforming to this interface will be responsible for formatting
    representations of objects that pass through sys.displayhook() during an
    interactive interpreter session.
    """

    # The kind of formatter.
    kind = 'display'

    # The unique identifier for this formatter.
    identifier = None


    def __call__(self, obj):
        """ Return a formatted representation of an object.

        Return None if one cannot return a representation in this format.
        """

        raise NotImplementedError


class ReprDisplayFormatter(IDisplayFormatter):
    """ Return the repr() string representation of an object.
    """

    # The unique identifier for this formatter.
    identifier = 'repr'

    
    def __call__(self, obj):
        """ Return a formatted representation of an object.
        """

        return repr(obj)


class PPrintDisplayFormatter(IDisplayFormatter):
    """ Return a pretty-printed string representation of an object.
    """

    # The unique identifier for this formatter.
    identifier = 'pprint'

    
    def __call__(self, obj):
        """ Return a formatted representation of an object.
        """

        import pprint
        return pprint.pformat(obj)


