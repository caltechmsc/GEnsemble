# encoding: utf-8
# -*- test-case-name: ipython1.test.test_multiengine -*-
"""REST web service interface to an ITaskController
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

import cPickle as pickle
import xmlrpclib

from zope.interface import Interface, implements, Attribute
from twisted.internet import defer, reactor
from twisted.python import components, failure, log

from ipython1.kernel import httputil
from ipython1.external.twisted.web2 import server, channel
from ipython1.external.twisted.web2 import http, resource
from ipython1.external.twisted.web2 import responsecode, stream
from ipython1.external.twisted.web2 import http_headers

from ipython1.kernel import newserialized
from ipython1.kernel import error
from ipython1.kernel.task import ITaskController,\
                ISynchronousTaskController

#-------------------------------------------------------------------------------
# The Controller side of things
#-------------------------------------------------------------------------------

class IHTTPTaskRoot(Interface):
    pass


class HTTPTaskRoot(resource.Resource):
    
    addSlash = True
    
    
    def __init__(self, tc):
        self.stc = ISynchronousTaskController(tc)
        self.child_run = HTTPTaskRun(self.stc)
        self.child_abort = HTTPTaskAbort(self.stc)
        self.child_getresult = HTTPTaskGetResult(self.stc)
        self.child_registerclient = HTTPTaskRegisterClient(self.stc)
        self.child_unregisterclient = HTTPTaskUnregisterClient(self.stc)
    
    #def locateChild(self, request, segments):
    #    log.msg("Segments: " + repr(segments))
    #    return self, ()
    
    def renderHTTP(self, request):
        return http.Response(200, stream=stream.MemoryStream(repr(request)))
    

components.registerAdapter(HTTPTaskRoot,
    ITaskController,
    IHTTPTaskRoot)


class HTTPTaskBaseMethod(resource.Resource):
    
    def __init__(self, stc):
        self.stc = stc
        log.msg("Creating child resource...")
    
    def locateChild(self, request, segments):
        return self, ()
    
    def renderHTTP(self, request):
        return http.Response(200, stream=stream.MemoryStream(repr(request)))
    
    def buildRequestSummary(self, request):
        reply = """host: %r
port: %r
path: %r
prepath: %r
postpath: %r
args: %r
method: %r
headers: %r
""" % (request.host, request.port, request.path, request.prepath, 
       request.postpath, request.args, request.method, request.headers)
        return reply
    
    def packageSuccess(self, result):
        headers, data = httputil.serialize(result)
        response = http.Response(200, stream=stream.MemoryStream(data))
        for k, v in headers.iteritems():
            response.headers.addRawHeader(k, v)
        response.headers.setHeader('content-type', http_headers.MimeType('text', 'plain'))
        return response
    
    def packageFailure(self, f):
        f.cleanFailure()
        headers, data = httputil.serialize(f)
        response = http.Response(200, stream=stream.MemoryStream(data))
        for k, v in headers.iteritems():
            response.headers.addRawHeader(k, v)
        response.headers.setHeader('content-type', http_headers.MimeType('text', 'plain'))
        return response
    

class HTTPTaskRun(HTTPTaskBaseMethod):
    
    def renderHTTP(self, request):
        pTask = request.args['pTask'][0]
        try:
            task = pickle.loads(pTask)
        except Exception, e:
            return self.packageFailure(failure.Failure(e))
        else:
            # clientID = self.stc.registerClient()
            d = self.stc.run(task)
            d.addCallback(lambda r: self.packageSuccess(r))
            d.addErrback(lambda f: self.packageFailure(f))
            # self.stc.unregisterClient(clientID)
            return d
    

class HTTPTaskAbort(HTTPTaskBaseMethod):
    
    def renderHTTP(self, request):
        # XXX - fperez: I added a plain 'pass' here so the code would compile,
        # but I'm not sure what's supposed to be in here.
        pass
    

class HTTPTaskRegisterClient(HTTPTaskBaseMethod):
    
    def renderHTTP(self, request):
        clientID = self.stc.registerClient()
        return self.packageSuccess(clientID)
    

class HTTPTaskUnregisterClient(HTTPTaskBaseMethod):
    
    def http_POST(request):
        clientID = request.args.get('clientid')
        d = defer.execute(self.stc.unregisterClient)
        d.addBoth(self.packageSuccess, self.packageFailure)
        return d
    


class IHTTPTaskFactory(Interface):
    pass

    
def HTTPServerFactoryFromTaskController(multiengine):
    """Adapt an ITaskController to a HTTPServerFactory."""
    s = server.Site(IHTTPTaskRoot(multiengine))
    return channel.HTTPFactory(s)
    
    
components.registerAdapter(HTTPServerFactoryFromTaskController,
            ITaskController, IHTTPTaskFactory)
        

