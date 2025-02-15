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
import httplib2, urllib

from zope.interface import Interface, implements
from twisted.python import components, failure, log

from ipython1.kernel import httputil, error
from ipython1.external.twisted.web2 import server, channel
from ipython1.external.twisted.web2 import http, resource
from ipython1.external.twisted.web2 import stream
from ipython1.external.twisted.web2 import http_headers

from ipython1.kernel.task import ITaskController
from ipython1.kernel.taskclient import InteractiveTaskClient

#-------------------------------------------------------------------------------
# The Controller side of things
#-------------------------------------------------------------------------------

class IHTTPTaskRoot(Interface):
    pass


class HTTPTaskRoot(resource.Resource):
    
    implements(IHTTPTaskRoot)
    addSlash = True
    
    def __init__(self, tc):
        self.tc = tc
        self.child_run = HTTPTaskRun(self.tc)
        self.child_abort = HTTPTaskAbort(self.tc)
        self.child_getresult = HTTPTaskGetResult(self.tc)
    
    def renderHTTP(self, request):
        return http.Response(200, stream=stream.MemoryStream(repr(request)))
    

components.registerAdapter(HTTPTaskRoot,
    ITaskController,
    IHTTPTaskRoot)


class HTTPTaskBaseMethod(resource.Resource):
    
    def __init__(self, tc):
        self.tc = tc
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
        try:
            pTask = request.args['pTask'][0]
            task = pickle.loads(pTask)
        except Exception, e:
            return self.packageFailure(failure.Failure(e))
        else:
            d = self.tc.run(task)
            d.addCallbacks(self.packageSuccess, self.packageFailure)
            return d
    

class HTTPTaskAbort(HTTPTaskBaseMethod):
    
    def renderHTTP(self, request):
        try:
            taskID = int(request.args['taskID'][0])
        except Exception, e:
            return self.packageFailure(failure.Failure(e))
        else:
            d = self.tc.abort(taskID)
            d.addCallbacks(self.packageSuccess, self.packageFailure)
            return d
    

class HTTPTaskGetResult(HTTPTaskBaseMethod):
    
    def renderHTTP(self, request):
        try:
            taskID = int(request.args['taskID'][0])
        except Exception, e:
            return self.packageFailure(failure.Failure(e))
        else:
            d = self.tc.getTaskResult(taskID)
            d.addCallbacks(self.packageSuccess, self.packageFailure)
            return d
    

class IHTTPTaskControllerFactory(Interface):
    pass

    
def HTTPServerFactoryFromTaskController(multiengine):
    """Adapt an ITaskController to a HTTPServerFactory."""
    s = server.Site(IHTTPTaskRoot(multiengine))
    return channel.HTTPFactory(s)
    

components.registerAdapter(HTTPServerFactoryFromTaskController,
            ITaskController, IHTTPTaskControllerFactory)

        
#----------------------------------------------------------------------------
#   Client Side
#----------------------------------------------------------------------------

class HTTPTaskClient(object):
    """The Client object for connecting to a TaskController over HTTP"""
    
    
    def __init__(self, addr):
        """Create a client that will connect to addr.
        
        Once created, this class will autoconnect and reconnect to the
        controller as needed.
        
        :Parameters:
            addr : tuple
                The (ip, port) of the IMultiEngine adapted controller.
        """
        self.addr = addr
        self.url = 'http://%s:%s/' % self.addr
        self._server = httplib2.Http()
        self.block = True
    
    
    def _executeRemoteMethod(self, method, **kwargs):
        args = urllib.urlencode(httputil.strDict(kwargs))
        request = self.url+method+'/'+'?'+args
        header, response = self._server.request(request)
        # print request
        # print header
        # print response
        result = self._unpackageResult(header, response)
        return result
    
    def _unpackageResult(self, header, response):
        status = header['status']
        if status == '200':
            result = httputil.unserialize(header, response)
            return self._returnOrRaise(result)
        else:
            raise error.ProtocolError("Request Failed: %s:%s"%(status, response))
        
    def _returnOrRaise(self, result):
        if isinstance(result, failure.Failure):
            result.raiseException()
        else:
            return result
    
    ##########  Interface Methods  ##########
    
    def run(self, task):
        pTask = pickle.dumps(task,2)
        return self._executeRemoteMethod('run', pTask=pTask)
    
    def abort(self, taskID):
        return self._executeRemoteMethod('abort', taskID=taskID)
    
    def getTaskResult(self, taskID, block=None):
        return self._executeRemoteMethod('getresult', taskID=taskID)
    
        
class HTTPInteractiveTaskClient(HTTPTaskClient, InteractiveTaskClient):
    pass
