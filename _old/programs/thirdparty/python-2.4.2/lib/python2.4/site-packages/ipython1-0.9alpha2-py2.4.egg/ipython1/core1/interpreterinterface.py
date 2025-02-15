
class IInterpreter(object):
    """Declares the basic interface for the interpreter."""
    def __init__(self):
        """ """

        # Fields, some of these will actually be properties/traits

        #: The current prompt number
        self.prompt_number = 0
        

        #: The active string with delimiters to split input lines for tab
        #completion.
        self.completer_delimiters = ' \t\n`!@#$^&*()=+[{]}\\|;:\'",<>?'

    # XXX - This code is currently under construction
    # Client api
    def complete(self,text,line):
        """ """
        
    def execute(self, lines):
        """ Execute text in an IPython interpreter.
            
        :Parameters:

          lines : string
            The lines can contain IPython (including magic, etc.)  or Pure
            Python input.
        """
        
    def execute_macro(self,macro):
        """ Execute a macro object, consisting of repeating """

    def execute_python(self, lines):
        """ Execute text in an IPython interpreter.

        :Parameters:

          lines : string
            The lines must be valid pure Python input.
        """

    def ipmagic(self,magic,arg_s):
        """"""

    def ipsystem(self,arg_s):
        """"""
        
    def pull(self, *keys):
        """"""
        
    def push(self, **kwargs):
        """"""
        
    def reset(self):
        """"""

    def safe_execfile(self,fname,*where,**kw):
        """ """
        
    def set_hook(self,name,hook,*a,**k):
        """ """
        
    # 'code' api
    def object_find(self,oname):
        """ """
