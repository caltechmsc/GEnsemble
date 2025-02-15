# encoding: utf-8
# -*- test-case-name: ipython1.test.test_nodes -*-
"""The classes and interfaces for nodes and cells for use in notebooks
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

import zope.interface as zi
from IPython.genutils import time

# the classes for use in notebook.py
classes = ['TextCell', 'IOCell', 'ImageCell', 'Node']

#-------------------------------------------------------------------------------
# Node and Cell Interfaces
#-------------------------------------------------------------------------------

class ICell(zi.Interface):
    """The Basic Cell Interface, implemented by all Nodes and Cells"""
    
    parent = zi.Attribute("Node: The parent object of the cell")
    dateCreated = zi.Attribute("String: The date the cell was created")
    dateModified = zi.Attribute("String: The date the cell was most recently modified")
    tags = zi.Attribute("List of Strings: Tags used for searching")


class INode(ICell):
    """The Basic Node Interface"""
    
    children = zi.Attribute("Dict: the children of the node")
    
    def addChild(child, index=None):
        """adds `child` to the node after `index`, defaulting to the end"""
    
    def popChild(index):
        """removes the child at `index`"""
    


class ITextCell(ICell):
    """A Basic text cell"""
    
    text = zi.Attribute("String: the text of the cell")
    format = zi.Attribute("String: the formatting for the text")
    

class IIOCell(ICell):
    """A Basic I/O Cell"""
    
    input = zi.Attribute("String: input python code")
    output = zi.Attribute("String: The output of input")

class IImageCell(ICell):
    """A Basic Cell for images"""
    
    image = zi.Attribute("Image: The image object")



#-------------------------------------------------------------------------------
# Node and Cell Objects
#-------------------------------------------------------------------------------

# helper code for strings
def _padstr(n):
    return "%02i"%n

def strtime():
    return ":".join(map(_padstr, time.localtime()[:6]))

class Cell(object):
    """The base Cell class"""
    
    zi.implements(ICell)
    
    def _modify(self):
        self.dateModified = strtime()
        if self.parent is not None:
            self.parent._modify()
    
    def _setCreated(self, c):
        raise IOError("dateCreated cannot be changed")
    
    def _getCreated(self): return self._dateCreated
    
    def _setTags(self, tags):
        self._tags = tags
        self._modify()
    
    def _getTags(self):  return self._tags
    
    tags = property(_getTags, _setTags)
    dateCreated = property(_getCreated, _setCreated)
    
    def __init__(self, id, parent=None, tags=[]):
        self.id = id
        self.parent = parent
        self._dateCreated = strtime()
        self.dateModified = self.dateCreated
        self._tags = tags
    
    def addTags(self, **tags):
        self._tags.update(tags)
        self._modify()
    

class Node(Cell):
    """The basic Node class"""
    
    zi.implements(INode)
    
    className="Node"
    
    def __init__(self, id, parent=None, flags={}):
        
        self.children = []
        super(Node, self).__init__(parent, flags)
    
    def addChild(self, child, index=None):
        """add child at index, defaulting to the end"""
        if index is None:
            # add to end
            self.children.append(child)
            self._modify()
            return len(self.children) - 1
        elif index < len(self.children):
            self.children = self.children[:index]+[child]+self.children[index:]
            self._modify()
            return index
        else:
            raise IndexError
    
    def popChild(self, index):
        """remove and return child at index"""
        if index < len(self.children):
            self._modify()
            return self.children.pop(index)
        else:
            raise IndexError
    

class TextCell(Cell):
    """A Cell for text"""
    
    zi.implements(ITextCell)
    
    className="TextCell"
    
    def _setText(self, text):
        self._text = text
        self._modify()
    
    def _getText(self):  return self._text
    
    text = property(_getText, _setText)
    
    def __init__(self, id, text="", parent=None, tags=[]):
        super(TextCell, self).__init__(id, parent, tags)
        self._text = text
    

class IOCell(Cell):
    """A Cell for handling execution"""
    
    zi.implements(IIOCell)
    
    className="IOCell"
    
    def _setInput(self, inp):
        self._input = inp
        self._modify()
    
    def _getInput(self): return self._input
    
    def _setOutput(self, out):
        self._output = out
        self._modify()
    
    def _getOutput(self):  return self._output
    
    input = property(_getInput, _setInput)
    output = property(_getOutput, _setOutput)
    
    def __init__(self, id, input="", parent=None, tags=[]):
        self._input = input
        self._output = ""
        super(IOCell, self).__init__(id, parent, tags)
    


class ImageCell(Cell):
    """A Cell for holding images"""
    
    zi.implements(IImageCell)
    
    className="ImageCell"
    
    def _setImage(self, im):
        self._image = im
        self._modify()
    
    def _getImage(self): return self._image
    
    def __init__(self, id, im=None, parent=None, tags=[]):
        self._image = im
        super(ImageCell, self).__init__(id, parent, tags)
    

