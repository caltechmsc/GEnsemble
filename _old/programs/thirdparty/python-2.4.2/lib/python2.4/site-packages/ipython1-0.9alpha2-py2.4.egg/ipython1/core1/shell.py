# encoding: utf-8
# -*- test-case-name: ipython1.test.test_shell -*-
"""
The core IPython Shell
"""
__docformat__ = "restructuredtext en"
#-------------------------------------------------------------------------------
#       Copyright (C) 2005  Fernando Perez <fperez@colorado.edu>
#                           Brian E Granger <ellisonbg@gmail.com>
#                           Benjamin Ragan-Kelley <benjaminrk@gmail.com>
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
#-------------------------------------------------------------------------------

import pprint
import signal
import sys
import threading
import time

from code import InteractiveConsole, softspace
from StringIO import StringIO

from IPython.OutputTrap import OutputTrap
from IPython import ultraTB

from ipython1.kernel.error import NotDefined


class InteractiveShell(InteractiveConsole):
    """The Basic IPython Shell class.  
    
    This class provides the basic capabilities of IPython.  Currently
    this class does not do anything IPython specific.  That is, it is
    just a python shell.
    
    It is modelled on code.InteractiveConsole, but adds additional
    capabilities.  These additional capabilities are what give IPython
    its power.  
    
    The current version of this class is meant to be a prototype that guides
    the future design of the IPython core.  This class must not use Twisted
    in any way, but it must be designed in a way that makes it easy to 
    incorporate into Twisted and hook network protocols up to.  
    
    Some of the methods of this class comprise the official IPython core
    interface.  These methods must be tread safe and they must return types
    that can be easily serialized by protocols such as PB, XML-RPC and SOAP.
    Locks have been provided for making the methods thread safe, but additional
    locks can be added as needed.
      
    Any method that is meant to be a part of the official interface must also
    be declared in the kernel.coreservice.ICoreService interface.  Eventually
    all other methods should have single leading underscores to note that they
    are not designed to be 'public.'  Currently, because this class inherits
    from code.InteractiveConsole there are many private methods w/o leading
    underscores.  The interface should be as simple as possible and methods 
    should not be added to the interface unless they really need to be there.   
    
    Note:
    
    - For now I am using methods named put/get to move objects in/out of the
      users namespace.  Originally, I was calling these methods push/pull, but
      because code.InteractiveConsole already has a push method, I had to use
      something different.  Eventually, we probably won't subclass this class
      so we can call these methods whatever we want.  So, what do we want to
      call them?
    - We need a way of running the trapping of stdout/stderr in different ways.
      We should be able to i) trap, ii) not trap at all or iii) trap and echo
      things to stdout and stderr.
    - How should errors be handled?  Should exceptions be raised?
    - What should methods that don't compute anything return?  The default of 
      None?
    """

