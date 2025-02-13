# encoding: utf-8
"""This module contains the public API for working with a remote controller.

The classes defined in this module are dynamically imported based on a users
configuration file.  This allows things like the network protocol to be 
selected dynamically at run time.

Depending on the configuration files, one of the following RemoteController classes
will be imported into this module as RemoteController:

- `multienginevanilla.RemoteController` (the default)

For more information about RemoteController consult the docstrings of the 
particular RemoteController classe you are using.

Magic Functions:

- ``%px``
- ``%pn``
- ``%autopx``

Attributes:

- `defaultController`: The (ip,port) tuple of the default local controller.

Basic Usage
===========

1. Import the api module:

    >>> import ipython1.kernel.api as kernel

2. Then create a RemoteController object:

    >>> rc = kernel.RemoteController(('localhost',10000))

If you are running everything on your local machine with the defaults, you
can also do:

    >>> rc = kernel.RemoteController(kernel.defaultController)
    
3. Now see if you can connect and check the engines:

    >>> rc.connect()
    Connecting to controller:  ('127.0.0.1', 10105)
    >>> rc.getIDs()
    (0, 1, 2, 3)

4. You are ready to go.  Next, check out the execute, push and pull methods of
   RemoteController.

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

import ipython1.config.api as config
clientConfig = config.getConfigObject('client')

import ipython1.kernel.magic

RemoteController = clientConfig.RemoteController
"""The default RemoteController class obtained from config information."""

defaultRemoteController = (clientConfig.connectToRemoteControllerOn['ip'],
    clientConfig.connectToRemoteControllerOn['port'])
"""The (ip,port) tuple of the default controller."""

from ipython1.kernel.task import Task

TaskController = clientConfig.TaskController
"""The default TaskController class obtained from config information."""

defaultTaskController = (clientConfig.connectToTaskControllerOn['ip'],
    clientConfig.connectToTaskControllerOn['port'])
"""The (ip,port) tuple of the default task controller."""