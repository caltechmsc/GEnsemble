# encoding: utf-8
# -*- test-case-name: ipython1.test.test_multiengine -*-
"""XMLRPC Utilities
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

# import cPickle as pickle
import sys
import xmlrpclib
# import httplib
# import urllib
# import base64
# import socket

# import re, string, time, operator
import string
from types import *

from ipython1.kernel.error import ProtocolError
# from ipython1.external.twisted.web2 import server, channel
# from ipython1.external.twisted.web2 import http, resource
# from ipython1.external.twisted.web2 import responsecode, stream
# from ipython1.external.twisted.web2 import http_headers

#-------------------------------------------------------------------------------
# Actual Utilities
#-------------------------------------------------------------------------------

class Transport(xmlrpclib.Transport):
    """Handles an HTTP transaction to an XML-RPC server."""

    def __init__(self):
        self.connection = None

    # client identifier (may be overridden)
    user_agent = "xmlrpclib.py/%s (by www.pythonware.com)" % xmlrpclib.__version__

    ##
    # Send a complete request, and parse the response.
    #
    # @param host Target host.
    # @param handler Target PRC handler.
    # @param request_body XML-RPC request body.
    # @param verbose Debugging flag.
    # @return Parsed response.

    def _full_request(self, host, handler, request_body):
        self.send_request(handler, request_body)
        self.send_host(host)
        self.send_user_agent()
        self.send_content(request_body)
        

    def request(self, host, handler, request_body, verbose=0):
        # issue XML-RPC request

        self.make_connection(host)
        if verbose:
            self.connection.set_debuglevel(1)

        try:
            self._full_request(host,handler,request_body)
        except:
            # If anything goes wrong, retry by first closing the connection.
            # Any exceptions at this point are allowed to propagate out for
            # handling code to deal with them.
            try:
                self.connection.close()
                self._full_request(host,handler,request_body)
            except:
                last_type = sys.last_type.__name__
                msg=("Error connecting to the server, please recreate the "
                     "client.\n"
                     "The original internal error was:\n"
                     "%s: %s" % (last_type,sys.last_value)
                     )
                raise error.ConnectionError(msg)
        
        response = self.connection.getresponse()
        errcode = response.status
        errmsg = response.reason
        headers = response.msg

        if errcode != 200:
            raise ProtocolError(
                host + handler,
                errcode, errmsg,
                headers
                )

        self.verbose = verbose

        return self.parse_response(response)

    ##
    # Create parser.
    #
    # @return A 2-tuple containing a parser and a unmarshaller.

    def getparser(self):
        # get parser and unmarshaller
        return xmlrpclib.getparser()

    ##
    # Get authorization info from host parameter
    # Host may be a string, or a (host, x509-dict) tuple; if a string,
    # it is checked for a "user:pw@host" format, and a "Basic
    # Authentication" header is added if appropriate.
    #
    # @param host Host descriptor (URL or (URL, x509 info) tuple).
    # @return A 3-tuple containing (actual host, extra headers,
    #     x509 info).  The header and x509 fields may be None.

    def get_host_info(self, host):

        x509 = {}
        if isinstance(host, TupleType):
            host, x509 = host

        import urllib
        auth, host = urllib.splituser(host)

        if auth:
            import base64
            auth = base64.encodestring(urllib.unquote(auth))
            auth = string.join(string.split(auth), "") # get rid of whitespace
            extra_headers = [
                ("Authorization", "Basic " + auth)
                ]
        else:
            extra_headers = None

        return host, extra_headers, x509

    ##
    # Connect to server.
    #
    # @param host Target host.
    # @return A connection handle.

    def make_connection(self, host):
        # create a HTTP connection object from a host descriptor
        if self.connection is None:
            import httplib
            host, extra_headers, x509 = self.get_host_info(host)
            self.connection = httplib.HTTPConnection(host)

    ##
    # Send request header.
    #
    # @param connection Connection handle.
    # @param handler Target RPC handler.
    # @param request_body XML-RPC body.

    def send_request(self, handler, request_body):
        self.connection.putrequest("POST", handler)

    def putheader(self, header, *values):
        "The superclass allows only one value argument."
        self.connection.putheader(header, '\r\n\t'.join(values))

    ##
    # Send host name.
    #
    # @param connection Connection handle.
    # @param host Host name.

    def send_host(self, host):
        host, extra_headers, x509 = self.get_host_info(host)
        self.putheader("Host", host)
        if extra_headers:
            if isinstance(extra_headers, DictType):
                extra_headers = extra_headers.items()
            for key, value in extra_headers:
                # The HTTP subclass allowed for multiple header values
                self.putheader(key, value)

    ##
    # Send user-agent identifier.
    #
    # @param connection Connection handle.

    def send_user_agent(self):
        self.putheader("User-Agent", self.user_agent)

    ##
    # Send request body.
    #
    # @param connection Connection handle.
    # @param request_body XML-RPC request body.

    def send_content(self, request_body):
        self.putheader("Content-Type", "text/xml")
        self.putheader("Content-Length", str(len(request_body)))
        self.connection.endheaders()
        if request_body:
            self.connection.send(request_body)

    ##
    # Parse response (alternate interface).  This is similar to the
    # parse_response method, but also provides direct access to the
    # underlying socket object (where available).
    #
    # @param file Stream.
    # @param sock Socket handle (or None, if the socket object
    #    could not be accessed).
    # @return Response tuple and target method.

    def parse_response(self, response):
        # read response from input file/socket, and parse it

        p, u = self.getparser()

        while 1:
            data = response.read(1024)
            if not data:
                response.close()
                break
            if self.verbose:
                print "body:", repr(data)
            p.feed(data)

        p.close()

        return u.close()
