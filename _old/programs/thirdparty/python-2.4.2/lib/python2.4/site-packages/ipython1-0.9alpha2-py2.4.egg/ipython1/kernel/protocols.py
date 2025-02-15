# encoding: utf-8
"""Low level network protocols."""
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

import socket

import zope.interface as zi
from twisted.protocols import basic
from twisted.internet import protocol, interfaces

from ipython1.kernel import error

# Exception classes

class MessageSizeError(error.KernelError):
    """If a message exceeds a certain limit, this should be raised"""
    pass

#-------------------------------------------------------------------------------
# EnhancedNetstringReceiver
#-------------------------------------------------------------------------------

class NetstringProducer(object):
    """A producer for sending large Netstrings."""
    
    zi.implements(interfaces.IProducer)
    
    def __init__(self, consumer, d):
        self.consumer = consumer
        self.d = d
        self.consumer.registerProducer(self, False)
        
        
    def resumeProducing(self):
        pass
        
    def stopProducing(self):
        pass
        
    def pauseProducingv(self):
        pass

class EnhancedNetstringReceiver(basic.NetstringReceiver, object):
    """This class provides some basic enhancements of NetstringReceiver."""
    
    MAX_LENGTH = 50*1024*1024                  # 50 MB
    
    def sendBuffer(self, buf):
        prefix = '%i:' %len(buf)
        if len(prefix)+len(buf) >= self.MAX_LENGTH:
            raise MessageSizeError
        self.transport.write(prefix)
        # want to be able to call:
        # self.transport.write(buf)
        # but can't, so we have a
        # temporary solution that copies:
        self.transport.write(str(buf))
        self.transport.write(',')
    
    def sendString(self, string):
        prefix = '%i:' %len(string)
        if len(prefix)+len(string) >= self.MAX_LENGTH:
            raise MessageSizeError
        return basic.NetstringReceiver.sendString(self, string)

class EnhancedFactory:
    """A Factory for the EnhancedNetstringReceiver that sets MAX_LENGTH."""
    
    MAX_LENGTH = 50*1024*1024                   # 50 MB
    
    def buildProtocol(self, addr):
        p = self.protocol()
        p.MAX_LENGTH = self.MAX_LENGTH
        p.factory = self
        return p
    

class EnhancedServerFactory(EnhancedFactory, protocol.ServerFactory, object):
    """Client Factory for EnhancedNetstrings."""
    pass

class EnhancedClientFactory(EnhancedFactory, protocol.ClientFactory, object):
    """Client Factory for EnhancedNetstrings."""
    pass


#-------------------------------------------------------------------------------
# A plain socket based netstring receiver
#-------------------------------------------------------------------------------
# Netstring code adapted from twisted.protocols.basic

class NetstringParseError(ValueError):
    """The incoming data is not in valid Netstring format."""
    pass



class NetstringSocket(object):
    """A wrapper for a socket that reads/writes Netstrings.
    
    This sends and receives strings over a socket, prefixing them with 
    a 4 byte integer specifying the length of the string.  This 4 byte
    integer is encoded in network byte order.
    
    Notes
    =====
        1. If extra data is received by this class it is discarded.
        2. This class might work with blocking/timeout'd sockets.
        3. No socket related exceptions are caught.
    """
    
    MAX_LENGTH = 50*1024*1024
    
    def __init__(self,sock):
        """Wrap a socket object for int32 prefixed reading/writing.
        
        The wrapped socket must be setup already.
        """
        self.sock = sock
        self._readerLength = 0
        self.__data = ''
        self.__buffer = ''
        self.verbose = False
    
    def writeNetstring(self,data):
        """Writes data to the socket.
        
        Notes
        =====
        
            1. This method uses buffers so substrings are not copied.
            2. No errors are caught currently.
        """
        if self.verbose: 
            print "client:",data
        prefix = "%i:" % len(data)
        
        if len(prefix)+len(data) >= self.MAX_LENGTH:
            raise MessageSizeError()
        
        offset = 0
        lengthToSend = len(prefix)
        while offset < lengthToSend:
            slice = buffer(prefix, offset, lengthToSend - offset)
            amountWritten = self.sock.send(slice)
            offset += amountWritten
            
        offset = 0
        lengthToSend = len(data)
        while offset < lengthToSend:
            slice = buffer(data, offset, lengthToSend - offset)
            if self.verbose:
                print lengthToSend, offset, len(slice), slice
            amountWritten = self.sock.send(slice)
            # print amountWritten
            offset += amountWritten
        
        return self.sock.send(',')
    
    
    def recvData(self):
        buffer,self.__data = self.__data[:self._readerLength],self.__data[self._readerLength:]
        self._readerLength = self._readerLength - len(buffer)
        self.__buffer = self.__buffer + buffer
        if self._readerLength != 0:
            return False
        else:
            return True
    
    def recvComma(self):
        if self.__data[0] != ',':
            raise NetstringParseError(repr(self.__data))
        self.__data = self.__data[1:]
        return True
    
    def recvLength(self):
        colon = self.__data.find(':')
        if colon == -1:
            return False
        try:
            self._readerLength = int(self.__data[:colon])
        except TypeError:
            return False
        else:
            self.__data = self.__data[colon+1:]
            return True
    
        
    def readNetstring(self, size=2048):
        """Reads a Netstring from the socket.
        
        Notes
        =====
            1. If there is an error, an error message is printed and
                an empty string is returned.  Change over to using exceptions.
            2. The received data is stored in a list to avoid copying strings.
            3. No socket related errors are caught currently.
        """
        # Read until we have at least 4 bytes
        while not self.recvLength():
            self.__data += self.sock.recv(size)
        while not self.recvData():
            self.__data += self.sock.recv(size)
        while not self.recvComma():
            self.__data += self.sock.recv(size)
        string = self.__buffer
        self.__buffer = ''
        if self.verbose:
            print "controller:",string
        return string

    
    