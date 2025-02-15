# encoding: utf-8
"""The IPython1 kernel.

The IPython kernel actually refers to three things:

 - The IPython Engine
 - The IPython Controller
 - Clients to the IPython Controller

The kernel module implements the engine, controller and client and all the 
network protocols needed for the various entities to talk to each other.

An end user should probably begin by looking at the `kernel.api` module.
"""
#-------------------------------------------------------------------------------
#       Copyright (C) 2005  Fernando Perez <fperez@colorado.edu>
#                           Brian E Granger <ellisonbg@gmail.com>
#                           Benjamin Ragan-Kelley <benjaminrk@gmail.com>
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
#-------------------------------------------------------------------------------