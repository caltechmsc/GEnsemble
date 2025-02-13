# Author:    Lisandro Dalcin
# Contact:   dalcinl@users.sourceforge.net
# Revision:  $Revision$
# Date:      $Date$
# Copyright: This module has been placed in the public domain.

"""
This is the **MPI for Python** package.

What is MPI?
============

MPI, the *Message Passing Interface*, is a standardized and portable
message-passing system designed to function on a wide variety of
parallel computers. The standard defines the syntax and semantics of
library routines and allows users to write portable programs in the
main scientific programming languages (Fortran, C, or C++).

Since its release, the MPI specification has become the leading
standard for message-passing libraries for parallel computers.
Implementations are available from vendors of high-performance
computers and from well known open source projects.

Package Structure
=================

Modules:

- MPI:      Message Passing Interface module.

- MPU:      Utilities and MPI extensions specific to Python.

- libmpi:   MPI basic types and C API module.

"""

__docformat__ = 'reStructuredText'

__author__    = 'Lisandro Dalcin'
__credits__   = 'MPI Forum, MPICH Team, Open MPI Team.'
__date__      = '13 Oct 2006'
__version__   = '0.4.0'
__revision__  = '$Id: __init__.py 16 2006-11-11 23:02:20Z dalcinl $'

__all__ = ['MPI', 'MPU', 'libmpi']
