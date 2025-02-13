class IInterpreter(object):
    """Declares the basic interface for the interpreter."""

    # XXX - This code is currently under construction
    # Client api
    def complete(self,text):
        """"""
        
    def execute(self, lines):
        """"""
        
    def execute_macro(self,macro):
        """"""

    def execute_python(self, lines):
        """"""

    def ipmagic(self,arg_s):
        """"""

    def ipsystem(self,arg_s):
        """"""

    def pull(self, key):
        """"""
        
    def push(self, **kwargs):
        """"""

    def reset(self):
        """"""
        
    def safe_execfile(self,fname,*where,**kw):
        """"""
        
    def set_hook(self,name,hook,*a,**k):
        """"""
        
    # 'code' api
    def object_find(self,oname):
        """"""
