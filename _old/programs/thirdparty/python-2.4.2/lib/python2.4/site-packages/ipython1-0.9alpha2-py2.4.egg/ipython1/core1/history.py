""" Manage the input and output history of the interpreter.
"""

# Local imports.
from util import InputList


class History(object):
    """ An object managing the input and output history at the interpreter
    level.
    """

    def __init__(self, input_cache=None, output_cache=None):

        # Stuff that IPython adds to the namespace.
        self.namespace_additions = dict(
            _ = None,
            __ = None,
            ___ = None,
        )

        # A list to store input commands.
        if input_cache is None:
            input_cache = InputList([''])
        self.input_cache = input_cache

        # A dictionary to store trapped output.
        if output_cache is None:
            output_cache = {}
        self.output_cache = output_cache

    def setup_namespace(self, namespace):
        """ Add the input and output caches into the interpreter's namespace
        with IPython-conventional names.

        Parameters
        ----------
        namespace : dict
        """

        namespace['In'] = self.input_cache
        namespace['_ih'] = self.input_cache
        namespace['Out'] = self.output_cache
        namespace['_oh'] = self.output_cache

    def update_history(self, interpreter, python):
        """ Update the history objects that this object maintains and the
        interpreter's namespace.

        Parameters
        ----------
        interpreter : Interpreter
        python : str
            The real Python code that was translated and actually executed.
        """

        number = interpreter.current_cell_number

        new_obj = interpreter.display_trap.obj
        if new_obj is not None:
            self.namespace_additions['___'] = self.namespace_additions['__']
            self.namespace_additions['__'] = self.namespace_additions['_']
            self.namespace_additions['_'] = new_obj
            self.output_cache[number] = new_obj

        interpreter.user_ns.update(self.namespace_additions)
        self.input_cache.add(number, python)
