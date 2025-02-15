# Standard library imports.
import sys
import compiler
from compiler.ast import Discard
import codeop
import __builtin__

# Local imports.
from ipython1.external.Itpl import ItplNS
from display_trap import DisplayTrap
from macro import Macro
from traceback_trap import TracebackTrap
from util import Bunch, system_shell

# Temporarily use this until it is ported to ipython1
from IPython import ultraTB
import pprint

def default_display_formatters():
    """ Return a list of default display formatters.
    """

    from display_formatter import PPrintDisplayFormatter, ReprDisplayFormatter
    return [PPrintDisplayFormatter(), ReprDisplayFormatter()]

def default_traceback_formatters():
    """ Return a list of default traceback formatters.
    """

    from traceback_formatter import PlainTracebackFormatter
    return [PlainTracebackFormatter()]


# XXX - experimental code to try to send exceptions over the wire with better
# information... Doesn't really work yet. - fperez
## import new
## def ewrap(evalue,msg):
##     evalue.message = msg
##     def __str__(self):
##         return self.__ipython_message
    
##     evalue.__str__ = new.instancemethod(__str__,evalue,evalue.__class__)


class Interpreter(object):
    """ An interpreter object.

    fixme: needs to negotiate available formatters with frontends.
    """

    def __init__(self, namespace=None, translator=None, magic=None,
        display_formatters=None, traceback_formatters=None, output_trap=None,
        history=None, message_cache=None, filename='<string>', config=None):

        # The namespace.
        if namespace is None:
            namespace = {}
        self.namespace = namespace

        # An object that will translate commands into executable Python.
        # The current translator does not work properly so for now we are going
        # without!
        # if translator is None:
        #             from ipython1.core.translator import IPythonTranslator
        #             translator = IPythonTranslator()
        self.translator = translator

        # An object that maintains magic commands.
        if magic is None:
            from ipython1.core.magic import Magic
            magic = Magic(self)
        self.magic = magic

        # A list of formatters for the displayhook.
        if display_formatters is None:
            display_formatters = default_display_formatters()
        self.display_formatters = display_formatters

        # A list of formatters for tracebacks.
        if traceback_formatters is None:
            traceback_formatters = default_traceback_formatters()
        self.traceback_formatters = traceback_formatters

        # The object trapping stdout/stderr.
        if output_trap is None:
            from ipython1.core.output_trap import OutputTrap
            output_trap = OutputTrap()
        self.output_trap = output_trap

        # An object that manages the history.
        if history is None:
            from ipython1.core.history import History
            history = History()
        self.history = history

        # An object that caches all of the return messages.
        if message_cache is None:
            from ipython1.core.message_cache import SimpleMessageCache
            message_cache = SimpleMessageCache()
        self.message_cache = message_cache

        # The "filename" of the code that is executed in this interpreter.
        self.filename = filename

        # An object that contains much configuration information.
        if config is None:
            # fixme: Move this constant elsewhere!
            config = Bunch(ESC_MAGIC='%')
        self.config = config

        # Hook managers.
        # fixme: make the display callbacks configurable. In the meantime,
        # enable macros.
        self.display_trap = DisplayTrap(
            formatters=self.display_formatters,
            callbacks=[self._possible_macro],
        )
        self.traceback_trap = TracebackTrap(
            formatters=self.traceback_formatters)

        # This is used temporarily for reformating exceptions in certain
        # cases.  It will go away once the ultraTB stuff is ported
        # to ipython1
        self.tbHandler = ultraTB.FormattedTB(color_scheme='NoColor',
                                                 mode='Context',
                                                 tb_offset=2)

        # An object that can compile commands and remember __future__
        # statements.
        self.command_compiler = codeop.CommandCompiler()

        # A replacement for the raw_input() and input() builtins. Change these
        # attributes later to configure them.
        self.raw_input_builtin = raw_input
        self.input_builtin = input

        # The number of the current cell.
        self.current_cell_number = 1

        # This is the message dictionary assigned temporarily when running the
        # code.
        self.message = None

        self.setup_namespace()


    #### Public 'Interpreter' interface ########################################

    def formatTraceback(self, et, ev, tb, message=''):
        """Put a formatted version of the traceback into value and reraise.
        
        When exceptions have to be sent over the network, the traceback 
        needs to be put into the value of the exception in a nicely
        formatted way.  The method takes the type, value and tb of an 
        exception and puts a string representation of the tb into the 
        value of the exception and reraises it.
        
        Currently this method uses the ultraTb formatter from IPython trunk.
        Eventually it should simply use the traceback formatters in core
        that are loaded into self.tracback_trap.formatters.
        """
        tbinfo = self.tbHandler.text(et,ev,tb)

        nv = ["""\
%s
***************************************************************************
Exception in the IPython Engine.""" % ev]

        if message:
            nv.append("""

Engine action that caused the error:

%s

""" % message )
        nv.append("""Full traceback:
%s
***************************************************************************
        """ % tbinfo)

        return et, ''.join(nv), tb
        
    def execute(self, commands, raiseException=True):
        """ Execute some IPython commands.

        1. Translate them into Python.
        2. Run them.
        3. Trap stdout/stderr.
        4. Trap sys.displayhook().
        5. Trap exceptions.
        6. Return a message object.

        Parameters
        ----------
        commands : str
            The raw commands that the user typed into the prompt.
        
        Returns
        -------
        message : dict
            The dictionary of responses. See the README.txt in this directory
            for an explanation of the format.
        """

        # Create a message dictionary with all of the information we will be
        # returning to the frontend and other listeners.
        message = dict(number=self.current_cell_number)

        # Massage the input and store the raw and translated commands into
        # a dict.
        input = dict(raw=commands)
        if self.translator is not None:
            python = self.translator(commands, message)
            if python is None:
                # Something went wrong with the translation. The translator
                # should have added an appropriate entry to the message object.
                return message
        else:
            python = commands
        input['translated'] = python
        message['input'] = input

        # Set the message object so that any magics executed in the code have
        # access.
        self.message = message

        # Set all of the output/exception traps.
        self.set_traps()
        
        # Actually execute the Python code.
        status = self.execute_python(python)

        # Unset all of the traps.
        self.unset_traps()

        # Unset the message object.
        self.message = None

        # Update the history variables in the namespace.
        # E.g. In, Out, _, __, ___
        if self.history is not None:
            self.history.update_history(self, python)

        # Let all of the traps contribute to the message and then clear their
        # stored information.
        self.output_trap.add_to_message(message)
        self.output_trap.clear()
        self.display_trap.add_to_message(message)
        self.display_trap.clear()
        self.traceback_trap.add_to_message(message)
        # Pull out the type, value and tb of the current exception
        # before clearing it.
        einfo = self.traceback_trap.args
        self.traceback_trap.clear()
        
        # Cache the message.
        self.message_cache.add_message(self.current_cell_number, message)

        # Bump the number.
        self.current_cell_number += 1
        
        # This conditional lets the execute method either raise any
        # exception that has occured in user code OR return the message
        # dict containing the traceback and other useful info.
        if raiseException and einfo:
            raise einfo[0],einfo[1],einfo[2]
        else:
            return message

    def execute_python(self, python):
        """ Actually run the Python code in the namespace.

        Parameters
        ----------
        python : str
            Pure, exec'able Python code. Special IPython commands should have
            already been translated into pure Python.
        """

        # We use a CommandCompiler instance to compile the code so as to keep
        # track of __future__ imports.
        try:
            commands = self.split_commands(python)
        except (SyntaxError, IndentationError), e:
            # The code has incorrect syntax. Return the exception object with
            # the message.
            self.message['syntax_error'] = e
            # Save the exc_info so compilation related exceptions can be
            # reraised
            self.traceback_trap.args = sys.exc_info()
            return

        for cmd in commands:
            try:
                code = self.command_compiler(cmd, self.filename, 'single')
            except (SyntaxError, OverflowError, ValueError), e:
                self.message['syntax_error'] = e
                self.traceback_trap.args = sys.exc_info()
            else:
                try:
                    exec code in self.namespace
                except:
                    self.traceback_trap.args = sys.exc_info()

    def execute_macro(self, macro):
        """ Execute the value of a macro.

        Parameters
        ----------
        macro : Macro
        """

        python = macro.value
        if self.translator is not None:
            python = self.translator(python)
        self.execute_python(python)

    def getCommand(self, i=None):
        """Gets the ith message in the message_cache.
        
        This is implemented here for compatibility with the old ipython1 shell
        I am not sure we need this though.  I even seem to remember that we
        were going to get rid of it.
        """
        return self.message_cache.get_message(i)

    def reset(self):
        """Reset the interpreter.
        
        Currently this only resets the users variables in the namespace.
        In the future we might want to also reset the other stateful
        things like that the Interpreter has, like In, Out, etc.
        """
        self.namespace = {}
        self.setup_namespace()

    def complete(self, text):
        # fixme: implement
        raise NotImplementedError

    def push(self, **kwds):
        """ Put value into the namespace with name key.
        
        Parameters
        ----------
        **kwds
        """          

        self.namespace.update(kwds)

    def pull(self, key):
        """ Get an item out of the namespace by key.
        
        Parameters
        ----------
        key : str

        Returns
        -------
        value : object

        Raises
        ------
        TypeError if the key is not a string.
        NameError if the object doesn't exist.
        """
        
        class NotDefined(object):
            pass
        
        if not isinstance(key, str):
            raise TypeError("Objects must be keyed by strings.")
        # Get the value this way in order to check for the presence of the key
        # and obtaining it actomically. No locks!
        result = self.namespace.get(key, NotDefined())
        if isinstance(result, NotDefined):
            raise NameError('name %s is not defined' % key)
        else:
            return result


    #### Interactive user API ##################################################

    def ipsystem(self, command):
        """ Execute a command in a system shell while expanding variables in the
        current namespace.

        Parameters
        ----------
        command : str
        """

        # Expand $variables.
        command = self.var_expand(command)

        system_shell(command,
            header='IPython system call: ',
            verbose=self.rc.system_verbose,
        )

    def ipmagic(self, arg_string):
        """ Call a magic function by name.

        ipmagic('name -opt foo bar') is equivalent to typing at the ipython
        prompt:

        In[1]: %name -opt foo bar

        To call a magic without arguments, simply use ipmagic('name').

        This provides a proper Python function to call IPython's magics in any
        valid Python code you can type at the interpreter, including loops and
        compound statements.  It is added by IPython to the Python builtin
        namespace upon initialization.

        Parameters
        ----------
        arg_string : str
            A string containing the name of the magic function to call and any
            additional arguments to be passed to the magic.

        Returns
        -------
        something : object
            The return value of the actual object.
        """

        # Taken from IPython.

        args = arg_string.split(' ', 1)
        magic_name = args[0]
        magic_name = magic_name.lstrip(self.config.ESC_MAGIC)

        try:
            magic_args = args[1]
        except IndexError:
            magic_args = ''
        fn = getattr(self.magic, 'magic_'+magic_name, None)
        if fn is None:
            self.error("Magic function `%s` not found." % magic_name)
        else:
            magic_args = self.var_expand(magic_args)
            return fn(magic_args)


    #### Private 'Interpreter' interface #######################################

    def setup_namespace(self):
        """ Add things to the namespace.
        """

        self.namespace.setdefault('__name__', '__main__')
        self.namespace.setdefault('__builtins__', __builtin__)
        self.namespace['__IP'] = self
        if self.raw_input_builtin is not None:
            self.namespace['raw_input'] = self.raw_input_builtin
        if self.input_builtin is not None:
            self.namespace['input'] = self.input_builtin
        
        builtin_additions = dict(
            ipmagic=self.ipmagic,
        )
        __builtin__.__dict__.update(builtin_additions)

        if self.history is not None:
            self.history.setup_namespace(self.namespace)

    def set_traps(self):
        """ Set all of the output, display, and traceback traps.
        """

        self.output_trap.set()
        self.display_trap.set()
        self.traceback_trap.set()

    def unset_traps(self):
        """ Unset all of the output, display, and traceback traps.
        """

        self.output_trap.unset()
        self.display_trap.unset()
        self.traceback_trap.unset()

    def split_commands(self, python):
        """ Split multiple lines of code into discrete commands that can be
        executed singly.

        Parameters
        ----------
        python : str
            Pure, exec'able Python code.

        Returns
        -------
        commands : list of str
            Separate commands that can be exec'ed independently.
        """

        # compiler.parse treats trailing spaces after a newline as a
        # SyntaxError.  This is different than codeop.CommandCompiler, which
        # will compile the trailng spaces just fine.  We simply strip any
        # trailing whitespace off.  Passing a string with trailing whitespace
        # to exec will fail however.  There seems to be some inconsistency in
        # how trailing whitespace is handled, but this seems to work.
        python = python.strip()

        # The compiler module will parse the code into an abstract syntax tree.
        ast = compiler.parse(python)

        # Uncomment to help debug the ast tree
        # for n in ast.node:
        #     print n.lineno,'->',n
                
        # Each separate command is available by iterating over ast.node. The
        # lineno attribute is the line number (1-indexed) beginning the commands
        # suite.
        # lines ending with ";" yield a Discard Node that doesn't have a lineno
        # attribute.  These nodes can and should be discarded.  But there are
        # other situations that cause Discard nodes that shouldn't be discarded.
        # We might eventually discover other cases where lineno is None and have
        # to put in a more sophisticated test.
        linenos = [x.lineno-1 for x in ast.node if x.lineno is not None]

        # When we finally get the slices, we will need to slice all the way to
        # the end even though we don't have a line number for it. Fortunately,
        # None does the job nicely.
        linenos.append(None)
        lines = python.splitlines()

        # Create a list of atomic commands.
        cmds = []
        for i, j in zip(linenos[:-1], linenos[1:]):
            cmd = lines[i:j]
            if cmd:
                cmds.append('\n'.join(cmd)+'\n')

        return cmds

    def error(self, text):
        """ Pass an error message back to the shell.

        Preconditions
        -------------
        This should only be called when self.message is set. In other words,
        when code is being executed.

        Parameters
        ----------
        text : str
        """

        errors = self.message.get('IPYTHON_ERROR', [])
        errors.append(text)

    def var_expand(self, template):
        """ Expand $variables in the current namespace using Itpl.

        Parameters
        ----------
        template : str
        """

        return str(ItplNS(template, self.namespace))

    def _possible_macro(self, obj):
        """ If the object is a macro, execute it.
        """

        if isinstance(obj, Macro):
            self.execute_macro(obj)

