# encoding: utf-8
"""
Configuration objects for IPython.

This module contains classes that contain configuration information.  These
classes are subclasses of `base.Config` and define specific attributes that
are needed to configure a particular entity.  

These classes should not be instantiated directly by a user or developer.  
Instead, `api.getConfigObject` should be used to retrieve an instance.  
This ensures that only one config object of each class gets created in 
a given process.

The configuration objects are retrieved by key. A complete list of the classes 
and corresponding keys can be found at the bottom of this file in the 
`configClasses` dictionary.
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

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

from ipython1.config.base import Config
from ipython1.config.cutils import getIpythonDir
from twisted.spread import pb

#-------------------------------------------------------------------------------
# Default Port Values
#-------------------------------------------------------------------------------

enginePort = 10201
xmlrpcMEPort = 10105
pbTCPort = 10114
xmlrpcTCPort = 10113
httpMEPort = 8000
httpNBPort = 8008

#-------------------------------------------------------------------------------
# Shell Configuration
#-------------------------------------------------------------------------------

from ipython1.core.interpreter import Interpreter

class ShellConfig(Config):
    shellClass = Interpreter
    """The particular shell class to use.
    
    Right now there is only one: `core.InteractiveShell`, but by creating a 
    new shell class that implements the same api as this default the user
    can customize its behavior.  For instance, the user could make a shell
    that supports additional syntax.
    """
    
    shellImportStatement = ''
    
#-------------------------------------------------------------------------------
# Engine Configuration
#-------------------------------------------------------------------------------


from ipython1.kernel.enginepb import PBEngineClientFactory

class EngineConfig(Config):
    connectToControllerOn = {'ip': '127.0.0.1', 'port': enginePort}
    """The ip, port the controller is listening for engines on."""
    
    #engineClientProtocolInterface = IVanillaEngineClientFactory
    engineClientProtocolInterface = PBEngineClientFactory
    """The interface corresponding to the network protocol used to connect
    to the controller with."""


class MPIConfig(Config):
    """MPI Configuration information.
    
    The configuration for MPI is somewhat different from all the other
    configuration entities.  This is because the engine has to import
    a module that calls MPI_Init immediately upon starting - even before
    the command line options are parsed.  This means that the mpi setup
    cannot be controlled from the command line.  
    
    To get around this, ipengine does::
    
        config.updateConfigWithFile('mpirc.py')
    
    to get the MPI configuration information.  The mpirc.py file
    will be looked for in:
    
    1.  The cwd
    2.  The ~./ipython directory
    3.  In the IPYTHONDIR directory
    """

    mpiImportStatement = ''
    """The import statement that will be attempted in starting mpi.  
    
    Some common options are:
    
    - ``from mpi4py import MPI as mpi``:  For using mpi4py
    - ``from ipython1 import mpi``:  For using IPython1's basic MPI module.
      This module only calls MPI_Init and then defines mpi.rank and mpi.size.
      This is useful for the many cases you don't need the entire MPI API, 
      just to have a rank and size defined.  You could also probably use
      this approach to make MPI calls from C/C++ code.
      
    Users are free to make their own MPI modules to use in this way.  But
    those modules must to do things:
    
    1.  Call MPI_Init() in an appropriate manner upon being imported.
    2.  Define the size and rank attributes of the module.
    
    It is also a good idea to have MPI_Finalize called automatically when
    the Python interpreter is shut down.  For information about how to do
    this see the `ipython1.mpi` module or ``mpi4py``.
    """
    
#-------------------------------------------------------------------------------
# Controller Configuration
#-------------------------------------------------------------------------------

from ipython1.kernel.multienginexmlrpc import \
    IXMLRPCMultiEngineFactory

# We need to make httplib2 a dependency before putting this here!    
# from ipython1.kernel.multienginehttp import \
#     IHTTPMultiEngineFactory
    
from ipython1.kernel.enginepb import \
    IPBEngineServerFactory

from ipython1.kernel.taskxmlrpc import \
    IXMLRPCTaskControllerFactory

from ipython1.kernel.taskpb import \
     IPBTaskControllerFactory

from ipython1.kernel.multiengine import IMultiEngine
from ipython1.kernel.task import ITaskController

# Setup network interfaces for the multiengine controller.

xmlrpcME = {'interface': IXMLRPCMultiEngineFactory, 
            'ip': '', 
            'port': xmlrpcMEPort}
            
# httpME = {'interface': IHTTPMultiEngineFactory, 
#           'ip': '', 
#           'port': httpMEPort}

# By default only the xmlprc interface is started.
networkInterfacesME = {
    'xmlrpc':xmlrpcME, 
    # 'http':httpME
    }

# Setup network interfaces for the task controller.

xmlrpcTC = {'interface':IXMLRPCTaskControllerFactory,
            'ip':'',
            'port':xmlrpcTCPort}

pbTC = {'interface': IPBTaskControllerFactory,
        'ip': '',
        'port': pbTCPort}

# By default only the xmlprc interface is started.
networkInterfacesTC = {
    'xmlrpc':xmlrpcTC,
    # 'pb': pbTC
    }


class ControllerConfig(Config):
    #engineServerProtocolInterface = IVanillaEngineServerFactory
    engineServerProtocolInterface = IPBEngineServerFactory
    """The interface for the network protocol for talking to engines."""
    
    listenForEnginesOn  = {'ip': '', 'port': enginePort}
    """The ip and port to listen for engine on."""
   
    controllerInterfaces = {'multiengine': {'controllerInterface': IMultiEngine, 
                                            'networkInterfaces': networkInterfacesME,
                                            'default': 'xmlrpc'},
                            'task' : {'controllerInterface': ITaskController, 
                                      'networkInterfaces': networkInterfacesTC,
                                      'default': 'xmlrpc'}}
    """Specify what how the controller is exposed.
    
    :Parameters:
        - `default`: for each controller interface determines which network
          interface will be controlled by command-line flags to ipcontroller.
    """
                                      
    controllerImportStatement = ''


#-------------------------------------------------------------------------------
# Client Configuration
#-------------------------------------------------------------------------------

# from ipython1.kernel.multienginepb import PBInteractiveMultiEngineClient

from ipython1.kernel.multienginexmlrpc import XMLRPCInteractiveMultiEngineClient

from ipython1.kernel.taskxmlrpc import XMLRPCInteractiveTaskClient

class ClientConfig(Config):    
    # RemoteController = PBInteractiveMultiEngineClient
    """The RemoteController class to use.
    
    This allow new RemoteController classes that use different network
    protocols to be used.
    """

    RemoteController = XMLRPCInteractiveMultiEngineClient
    
    connectToRemoteControllerOn = {'ip': '127.0.0.1', 'port': xmlrpcMEPort}
    """The (ip, port) tuple the client will use to connect to the controller."""
    
    TaskController = XMLRPCInteractiveTaskClient
    
    connectToTaskControllerOn = {'ip': '127.0.0.1', 'port': xmlrpcTCPort}
    
#-------------------------------------------------------------------------------
# Notebook Configuration
#-------------------------------------------------------------------------------

# from ipython1.kernel.multienginepb import PBInteractiveMultiEngineClient

try:
    from ipython1.kernel.engineservice import IEngineQueued
    from ipython1.notebook.notebook import NotebookController as NC
    from ipython1.notebook.notebookhttp import IHTTPNotebookServerFactory
except ImportError:
    NotebookConfig = None
else:
    class NotebookConfig(Config):    
        # RemoteController = PBInteractiveMultiEngineClient
        """The RemoteController class to use.
    
        This allow new RemoteController classes that use different network
        protocols to be used.
        """
    
        engineInterface = IEngineQueued
        networkInterfaces = {'http':{'interface': IHTTPNotebookServerFactory,
                                        'ip'    : '',
                                        'port'  : httpNBPort}}
        defaultDBMode = "sqlite///"
        activeDB = "sqlite:///%s/ipnotebooks.db"%(getIpythonDir())
        # activeDB = "sqlite://"
        # print activeDB
        externalDBs = []
    

# All top-level config classes must be listed here.

configClasses = {'engine'     : EngineConfig,
                 'controller' : ControllerConfig,
                 'notebook'   : NotebookConfig,
                 'client'     : ClientConfig,
                 'shell'      : ShellConfig,
                 'mpi'        : MPIConfig}



