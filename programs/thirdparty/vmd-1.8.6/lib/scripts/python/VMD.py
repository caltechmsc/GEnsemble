############################################################################
#cr
#cr            (C) Copyright 1995-2007 The Board of Trustees of the
#cr                        University of Illinois
#cr                         All Rights Reserved
#cr
############################################################################

############################################################################
# RCS INFORMATION:
#
#       $RCSfile: VMD.py,v $
#       $Author: johns $        $Locker:  $             $State: Exp $
#       $Revision: 1.12 $        $Date: 2007/03/03 19:54:47 $
#
############################################################################

"""
This module is import by VMD the first time gopython is called.  
The modules imported below comprise the entire Python interface
to VMD.
"""

version = 1.8

# These are the lowest level Python commands provided by VMD
import animate
import atomsel   # Replaces AtomSel and atomselection
import axes
import color
import display
import graphics
import imd
import label
import material
import molecule
import molrep
import mouse
import render
import trans
import vmdcallbacks
import vmdmenu

# These modules define classes for convenient manipulation of VMD state.
import Label
import Material
import Molecule

# This class is deprecated, so it s no longer automatically imported.
#import AtomSel

# The vmdnumpy module is available only if the Numeric Python module is
# installed on your system.
try:
  import vmdnumpy
except:
  pass

# helper function.
def __setupWindow(name, root):
  def cb(name=name):
    vmdmenu.show(name, 0)
  root.wm_protocol("WM_DELETE_WINDOW", cb)
  # Some window managers (e.g. KDE) don't remember the position of windows 
  # when they are closed until after wm_geometry() has been called.  So
  # we do it here.  Exception: on MacOS X, this workaround causes the
  # window to appear under the toolbar.
  import sys
  if sys.platform != 'darwin':
    root.wm_geometry("+%d+%d" % (root.winfo_x(), root.winfo_y()))

def addExtensionMenu(name, root):
  """
  Use this method to add an item to the VMD Extensions menu.  root should
  be a reference to a Tkinter.Tk() instance.  The WM_DELETE_WINDOW protocol 
  will be overridden to prevent the window from being destroyed.  
  """
  __setupWindow(name, root)
  return vmdmenu.add(name, root)

def registerExtensionMenu(name, func):
  """
  Use this method to register a function that creates the window for an
  extension.  func() will be called when the window is first requested
  to be opened.  The WM_DELETE_WINDOW protocol will also be overridden
  to prevent the window from being destroyed.  
  """
  def createFunc(name=name, func=func):
    root=func()
    __setupWindow(name, root)
    return root
  vmdmenu.register(name, createFunc)

import hotkeys

