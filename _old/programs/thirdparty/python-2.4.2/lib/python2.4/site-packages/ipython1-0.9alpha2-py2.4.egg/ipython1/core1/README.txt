This contains the implementation of a Python interpreter that provides IPython
functionality (magics, aliases, history, and all that jazz).


Message dictionaries
--------------------
The interpreter responds to a command with a dictionary of simple Python types,
anything that can be reliably serialized by basic serialization methods: no
instances. Interpreter subsystems can add data to this dictionary more or less
freely, and consumers of this message dictionary can use or ignore parts of it
relatively freely.

There are some standard entries in this dictionary:

'number' : int
    The number of the "cell" that this message refers to. This would be the
    number NN in the In[NN]: and Out[NN]: prompts in standard IPython.

'input' : dict
    The input from the user. It has the following entries:

    'raw' : str
        The string of commands that the user submitted to the interpreter.

    'translated' : str
        The string of pure, exec'able Python code that the translator subsystem
        derived from the user's input and actually executed.

'display' : dict
    When executing the input yields an object that is not None, it will be
    passed through the IDisplayFormatters that the interpreter has been
    configured with. This dictionary maps each formatter's identifier string to
    its results.

'stdout' : str, optional
    If executing the command resulted in printing anything out to stdout, this
    is what it printed.

'stderr' : str, optional
    If executing the command resulted in printing anything out to stderr, this
    is what it printed.

'traceback' : dict, optional
    If executing the command resulted in an exception, look 

'IPYTHON_ERROR' : list of str, optional
    Error messages internal to IPython.

'syntax_error' : SyntaxError instance, optional
    If there is a syntax error in the input, this is its exception object. It is
    separate from the 'traceback' entry because it happens before the code is
    executed, and the traceback formatters aren't going to be good for this kind
    of exception.
    # fixme: This could be put into traceback with a special formatter. Notably,
    # I'm not sure that SyntaxError instances are as serializable as we want the
    # message dictionary to be.  Importantly, we also have enough information to
    # actually locate the actual error in the code. Current Python/IPython
    # doesn't because the code isn't actually in a file. We can do better.
