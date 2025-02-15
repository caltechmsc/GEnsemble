# encoding: utf-8
"""Classes for using Apple's Bonjour with Twisted."""
__docformat__ = "restructuredtext en"
#*****************************************************************************
#       Copyright (C) 2005  Fernando Perez <fperez@colorado.edu>
#                           Brian E Granger <ellisonbg@gmail.com>
#                           Benjamin Ragan-Kelley <benjaminrk@gmail.com>
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
#*****************************************************************************

import bonjour

from twisted.internet.interfaces import IReadDescriptor
from twisted.internet import reactor
from twisted.python import log
from twisted.internet import defer
from twisted.spread import pb
from zope.interface import implements, classImplements

class BonjourError(Exception):
    """Bonjour Error"""
    
    def __init__(self, errorCode):
        self.errorCode = errorCode
    
    def __str__(self):
        return "Bonjour Error: %i" % self.errorCode
            
class BonjourRegistrationError(BonjourError):
    """Bonjour Registration Error"""
    
    def __str__(self):
        return "Bonjour Registration Error: %i" % self.errorCode    

class BonjourBrowseError(BonjourError):
    """Bonjour Browse Error"""
    
    def __str__(self):
        return "Bonjour Browse Error: %i" % self.errorCode    
           
class BonjourResolveError(BonjourError):
    """Bonjour Resolve Error"""
    
    def __str__(self):
        return "Bonjour Resolve Error: %i" % self.errorCode    

            
class BonjourDescriptor(object,log.Logger):
    """Integrates a Bonjour file desc. into the Twisted event loop.
    
    The user should not create instances of this class directly.  They
    should instead be created by the higher level classes like
    BonjourAdvertiser, BonjourBrowser, etc."""

    implements(IReadDescriptor)
    
    def __init__(self, fd, sdRef):
        """Wrap a Bonjour file descriptor
        
        @arg fd: file Descriptor to wrap
        @type fd: int
        @arg sdRef: Initialized ServiceDiscovery reference
        """
        self.fd = fd
        self.sdRef = sdRef
        
    def fileno(self):
        """Return the raw file descriptor"""
        return self.fd
        
    def doRead(self):
        """Called by the Twited event loop when the fd is ready to read."""
        ret = bonjour.DNSServiceProcessResult(self.sdRef)
        
    def connectionLost(self, reason):
        """Called by the Twisted event loop when things are shutting down."""
        log.msg("Stopping Bonjour Advertisement")
        if self.sdRef is not None:
            bonjour.DNSServiceRefDeallocate(self.sdRef)
            self.sdRef = None
        
        
class BonjourAdvertiser(object):
    """Advertise a service using Bonjour."""
    
    def __init__(self, name, regtype, port, callback, reactor,
                 flags=0, interfaceIndex=0, domain='local',host='', 
                 txtLen=0, txtRecord=None, context=None):
        """Create an object to advertise a Bonjour service.
        
        It will call the callback when there is a Bonjour event.  The callback
        should have the following arguments:
        
        def callback(sdRef,flags,errorCode,name,regtype,domain,context):
        
        The callback could be called more than once.
        
        @arg name: The name of the service
        @type name: str
        @arg regtype: The type of service, like _http._tcp
        @type regtype: str
        @arg domain: The Bonjour domain to browse, like local
        @type domain: str
        @arg port: The port to advertise as
        @type port: int
        @arg reactor: The Twisted reactor
        """
        
        self.name = name
        self.regtype = regtype
        self.domain = domain
        self.port = port
        self.reactor = reactor
        self.callback = callback
        self.flags = flags
        self.interfaceIndex = interfaceIndex
        self.host = host
        self.txtLen = txtLen
        self.txtRecord = txtRecord
        self.context = context
        
    def startAdvertising(self):
        """Advertise the service with Bonjour.
        
        This method returns a deferred.  Upon success, the result
        is a dictionary of information about the service.  Upon failure,
        the result is a Failure object that knows the BonjourError code.
        """
        
        # Allocate a Bonjour Service Reference
        self.sdRef = bonjour.AllocateDNSServiceRef()
        
        # Initiate Registration of the service
        ret = bonjour.pyDNSServiceRegister(self.sdRef,
            self.flags,
            self.interfaceIndex,
            self.name,
            self.regtype,
            self.domain,
            self.host,
            self.port,
            self.txtLen,
            self.txtRecord,
            self.callback,
            self.context)
                        
        # Error check for immediate failure
        if ret != bonjour.kDNSServiceErr_NoError:
            raise BonjourRegistrationError(ret)
            
        # Get the file descriptor and integrate with twisted
        self.fd = bonjour.DNSServiceRefSockFD(self.sdRef)
        self.bonjourDesc = BonjourDescriptor(self.fd, self.sdRef)
        self.reactor.addReader(self.bonjourDesc)
        
        return None
        
    def stopAdvertising(self):
        """Stop advertising the service."""
        
        # Remove the Reader Deallocate the serviceReference
        self.reactor.removeReader(self.bonjourDesc)
        if self.sdRef is not None:
            bonjour.DNSServiceRefDeallocate(self.sdRef)
            self.sdRef = None

class BonjourBrowser(object):
    """Browse for a Bonjour advertised service."""
    
    def __init__(self, regtype, callback, reactor,
                 flags=0, interfaceIndex=0, domain='local', 
                 context=None):
        """Create an object to browse for a Bonjour service.
        
        It will call the callback when there is a Bonjour event.  The callback
        should have the following arguments:
        
        def callback(sdRef,flags,interfaceIndex,errorCode,
                      name,regtype,domain,context):
        
        The callback could be called more than once.
        
        @arg name: The name of the service
        @type name: str
        @arg regtype: The type of service, like _http._tcp
        @type regtype: str
        @arg domain: The Bonjour domain to browse, like local
        @type domain: str
        @arg port: The port to advertise as
        @type port: int
        @arg reactor: The Twisted reactor
        """
        
        self.regtype = regtype
        self.domain = domain
        self.reactor = reactor
        self.callback = callback
        self.flags = flags
        self.interfaceIndex = interfaceIndex
        self.context = context
        
    def startBrowsing(self):
        """Advertise the service with Bonjour.
        
        This method returns a deferred.  Upon success, the result
        is a dictionary of information about the service.  Upon failure,
        the result is a Failure object that knows the BonjourError code.
        """
        
        # Allocate a Bonjour Service Reference
        self.sdRef = bonjour.AllocateDNSServiceRef()
        
        # Initiate Registration of the service
        ret = bonjour.pyDNSServiceBrowse(self.sdRef,
            self.flags,
            self.interfaceIndex,
            self.regtype,
            self.domain,
            self.callback,
            self.context)
                        
        # Error check for immediate failure
        if ret != bonjour.kDNSServiceErr_NoError:
            raise BonjourBrowseError(ret)
            
        # Get the file descriptor and integrate with twisted
        self.fd = bonjour.DNSServiceRefSockFD(self.sdRef)
        self.bonjourDesc = BonjourDescriptor(self.fd, self.sdRef)
        self.reactor.addReader(self.bonjourDesc)
        
        return None
        
    def stopBrowsing(self):
        """Stop advertising the service."""
        
        # Remove the Reader Deallocate the serviceReference
        self.reactor.removeReader(self.bonjourDesc)
        if self.sdRef is not None:
            bonjour.DNSServiceRefDeallocate(self.sdRef)
            self.sdRef = None

class BonjourResolver(object):
    """Resolve a Bonjour service."""
    
    def __init__(self, name, regtype, callback, reactor,
                 flags=0, interfaceIndex=0, domain='local', 
                 context=None):
        """Create an object to resolve a Bonjour service.
        
        It will call the callback when there is a Bonjour event.  The callback
        should have the following arguments:
        
        def callback(sdRef,flags,interfaceIndex,errorCode,
                      fullname,hosttarget,port,txtLen,txtRecord,context):
        
        The callback could be called more than once.
        
        @arg name: The name of the service
        @type name: str
        @arg regtype: The type of service, like _http._tcp
        @type regtype: str
        @arg domain: The Bonjour domain to browse, like local
        @type domain: str
        @arg port: The port to advertise as
        @type port: int
        @arg reactor: The Twisted reactor
        """
        
        self.name = name
        self.regtype = regtype
        self.domain = domain
        self.reactor = reactor
        self.callback = callback
        self.flags = flags
        self.interfaceIndex = interfaceIndex
        self.context = context
        
    def startResolving(self):
        """Advertise the service with Bonjour.
        
        This method returns a deferred.  Upon success, the result
        is a dictionary of information about the service.  Upon failure,
        the result is a Failure object that knows the BonjourError code.
        """
        
        # Allocate a Bonjour Service Reference
        self.sdRef = bonjour.AllocateDNSServiceRef()
        
        # Initiate Registration of the service
        ret = bonjour.pyDNSServiceResolve(self.sdRef,
            self.flags,
            self.interfaceIndex,
            self.name,
            self.regtype,
            self.domain,
            self.callback,
            self.context)
                        
        # Error check for immediate failure
        if ret != bonjour.kDNSServiceErr_NoError:
            raise BonjourResolveError(ret)
            
        # Get the file descriptor and integrate with twisted
        self.fd = bonjour.DNSServiceRefSockFD(self.sdRef)
        self.bonjourDesc = BonjourDescriptor(self.fd, self.sdRef)
        self.reactor.addReader(self.bonjourDesc)
        
        return None
        
    def stopResolving(self):
        """Stop advertising the service."""
        
        # Remove the Reader Deallocate the serviceReference
        self.reactor.removeReader(self.bonjourDesc)
        if self.sdRef is not None:
            bonjour.DNSServiceRefDeallocate(self.sdRef)
            self.sdRef = None

class PBServerFactoryBonjour(pb.PBServerFactory):
    """A replacement for PBServerFactory that enables Bonjour Registration."""

    def __init__(self, root, serviceName, 
                 serviceType, servicePort, unsafeTracebacks=False):
        
        pb.PBServerFactory(root, unsafeTracebacks)
        self.serviceName = serviceName
        self.serviceType = serviceType
        self.servicePort = servicePort
        
    def startFactory(self):
        self.ba = BonjourAdvertiser(self.serviceName,
                                    self.serviceType,
                                    self.servicePort,
                                    self.registrationCallback,
                                    reactor)
                                    
        self.ba.startAdvertising()
        
    def stopFactory(self):
        self.ba.stopAdvertising()
    
    def registrationCallback(self, sdRef,flags,errorCode,name,
                     regtype,domain,context):
        if errorCode == bonjour.kDNSServiceErr_NoError:
            print errorCode, name, regtype, domain
        else:
            print "Bonjour registration error"

#def listenTCP(port, factory, backlog=50, interface='', serviceName):
#    def listenTCP(self, port, factory, backlog=50, interface='')