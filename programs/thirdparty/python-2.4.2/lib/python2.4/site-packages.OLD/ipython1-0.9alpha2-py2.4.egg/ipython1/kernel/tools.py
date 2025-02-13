# encoding: utf-8
"""
This module contains tools for doing interactive parallel work.

The functions and classes here are designed to be imported and used on Engines
that have a rank and size defined.  The functions here use these to determine
how to partition lists and arrays amongst the Engines.
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

import sys
import os

#-------------------------------------------------------------------------------
# Utilities
#-----------------------------------------------------------------------------

_size = None
_rank = None

def setSizeAndRank(s, r):
    global _size
    global _rank
    print "setting s,r: ", s, r
    _size = s
    _rank = r

def getSizeAndRank():
    return _size, _rank
    
def getPartitionIndices(p, q, seqLength):
    """Return the lo, hi indices of the pth partition of a sequence of len q."""
    
    # Test for error conditions here
    if p<0 or p>=q:
      print "No partition exists."
      return
      
    remainder = seqLength%q
    basesize = seqLength/q
    hi = []
    lo = []
    for n in range(q):
        if n < remainder:
            lo.append(n * (basesize + 1))
            hi.append(lo[-1] + basesize + 1)
        else:
            lo.append(n*basesize + remainder)
            hi.append(lo[-1] + basesize)
            
    return lo[p], hi[p]
    
#-------------------------------------------------------------------------------
# Distributed versions of some standard Python datatypes.
#-------------------------------------------------------------------------------

def drange(start, stop, step=1):
    """A distributed range object."""
    
    size, rank = getSizeAndRank()
    if size is None or rank is None:
        print "First set the size and rank using setSizeAndRank."
        return
        
    totalLength = stop - start
    lo, hi = getPartitionIndices(rank, size, totalLength)
    return range(lo, hi)
        
#-------------------------------------------------------------------------------
# Distributed versions of numpy arrays.
#-------------------------------------------------------------------------------
    
try:
    import numpy
except ImportError:
    pass
else:
    def darange(start, stop, step):
        """A distributed version of arange."""
        
        size, rank = getSizeAndRank()
        if size is None or rank is None:
            print "First set the size and rank using setSizeAndRank."
            return
        
    def dlinspace(start, stop, n):
        """A distributed version of linspace."""
        
        size, rank = getSizeAndRank()
        if size is None or rank is None:
            print "First set the size and rank using setSizeAndRank."
            return
