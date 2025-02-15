# encoding: utf-8
# -*- test-case-name: ipython1.test.test_notebook_xmlutil -*-
"""The XML Representation of Notebook components
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

from ipython1.notebook import models, dbutil



# class parseLoader(object):
INPUTS = [">>>"]
CONTINUES = ["..."]
TEXTS = ['"""', "'''"]
CONTROLS = ["py-section", "py-section-end"]
    
# def __init__(self, user):
#     self.user = user
#     # self.session = session
#     self.sectionStack = []

def control(line):
    if line and line[0] == '#':
        splits = line.split(' ',2)
        if len(splits) > 1:
            if splits[1] in CONTROLS:
                if len(splits) > 2:
                    return splits[1], splits[2]
                else:
                    return splits[1] , ""
        return 'py-comment', line[1:]
    elif line[:3] in INPUTS:
        return 'py-input', line[4:]
    elif line[:3] in CONTINUES:
        return 'py-continue', line[4:]
    elif line[:3] in TEXTS:
        return line[:3], line[3:]
    return None, line

def readComments(inlines, comments=[]):
    # comments = []
    ctrl, line = control(inlines.pop(0))
    if ctrl == 'py-comment':
        comments.append(line)
    while inlines and ctrl in [None, 'py-comment']:
        ctrl, line = control(inlines.pop(0))
        if ctrl == 'py-comment':
            comments.append(line)
    return ctrl, line, comments

def readInput(inlines, inputs=[]):
    # lines = []
    ctrl, line = control(inlines.pop(0))
    while inlines and ctrl == 'py-continue':
        inputs.append(line)
        ctrl, line = control(inlines.pop(0))
    return ctrl, line, inputs

def readOutput(inlines, outputs=[]):
    # lines = []
    ctrl, line = control(inlines.pop(0))
    while inlines and ctrl is None and line[:4] == "    ":
        outputs.append(line[4:])
        ctrl, line = control(inlines.pop(0))
    return ctrl, line, outputs

def readText(inlines, end, textLines=[]):
    line = inlines.pop(0)
    while end not in line:
        textLines.append(line)
        line = inlines.pop(0)
    textLines.append(line[:line.find(end)])
    if line[line.find(end)+3:].strip():
        raise SyntaxError(line)
    return textLines


def loadNotebookFromSparse(session, user, s, fname=False):
    """user is a User, and s is either a filename or string.  fname
    is a flag to specify whether s is a filename, defaulting to False."""
    if fname:
        f = open(s)
        s = f.read()
        f.close()
    inlines = s.splitlines()
    filelen = len(inlines)
    sectionStack = []
    ctrl, line, comments = readComments(inlines)
    if ctrl != "py-section":
        nb = dbutil.createNotebook(session, user, "")
    else:
        nb = dbutil.createNotebook(session, user, line)
    nb.root.comment = '\n'.join(comments)
    sectionStack.append(nb.root)
    active = nb.root
    ctrl, line = control(inlines.pop(0))
    while inlines: # main parsing loop
        if ctrl is None:
            ctrl, line = control(inlines.pop(0))
        elif ctrl == 'py-comment': # read comments
            ctrl, line, comments = readComments(inlines, [line])
            if active.comment:
                comments = [active.comment]+comments
            active.comment = '\n'.join(comments)
        elif ctrl == 'py-section': # create a section
            active = models.Section(line)
            sectionStack[-1].addChild(active)
            session.flush()
            sectionStack.append(active)
            ctrl, line = control(inlines.pop(0))
        elif ctrl == 'py-section-end': # close a section
            sectionStack.pop()
            if sectionStack:
                active = sectionStack[-1]
            ctrl, line = control(inlines.pop(0))
        elif ctrl in TEXTS: # read a text block
            end = ctrl
            active = models.TextCell()
            sectionStack[-1].addChild(active)
            session.flush()
            if end in line:
                active.textData = line[:line.find(end)]
                if line[line.find(end)+3:].strip():
                    raise SyntaxError(line)
            else:
                textLines = readText(inlines, end, [line])
                active.textData = '\n'.join(textLines)
            ctrl, line = control(inlines.pop(0))
        elif ctrl == 'py-input':
            active = models.InputCell()
            sectionStack[-1].addChild(active)
            session.flush()
            ctrl, line, inputs = readInput(inlines, [line])
            active.input = '\n'.join(inputs)
            if ctrl == None and line[:4] == "    ":
                ctrl, line, outputs = readOutput(inlines, [line[4:]])
                active.output = '\n'.join(outputs)
        else:
            # I do not think this can happen
            raise SyntaxError("Parse Error, line %i: %s"%(filelen-len(inlines), line))
    
    return nb







