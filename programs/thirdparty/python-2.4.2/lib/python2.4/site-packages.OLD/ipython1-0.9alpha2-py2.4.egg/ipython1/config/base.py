# encoding: utf-8
"""
Configuration objects for IPython's configuration and customization.
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

import os
import sys
        
class Config(object):
    """A class that contains configuration data.
    
    The Config data class is designed to be a simple bag for configuration
    related data.  Eventually this class will be a subclass of 
    enthought.traits.HasTraits to allow for verification of  
    config data, but for now it is a simple class.
    
    This class is meant to serve as an abstract class.  Configuration objects
    for specific purposes will be suclasses of this class.  Examples can
    be found in `config.objects`.
    """
    def __setattr__(self, name, value):
        """This should print data as it is assigned, but it doesn't always."""
        print "Setting %s.%s to: " % (self.__class__, name), repr(value)
        self.__dict__[name] = value

    def update(self, **kwargs):
        """Update configuration attributes."""
        for k, v in kwargs.iteritems():
            if hasattr(self, k):
                print "Setting %s to: " % k + repr(v)
                setattr(self, k, v)
