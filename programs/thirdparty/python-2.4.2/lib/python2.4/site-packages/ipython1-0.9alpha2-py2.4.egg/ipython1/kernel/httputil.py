# encoding: utf-8
# -*- test-case-name: ipython1.test.test_multiengine -*-
"""HTTP Utilities
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
import httplib
import urllib
import base64

from ipython1.external.twisted.web2 import server, channel
from ipython1.external.twisted.web2 import http, resource
from ipython1.external.twisted.web2 import responsecode, stream
from ipython1.external.twisted.web2 import http_headers

from ipython1.kernel import newserialized


#-------------------------------------------------------------------------------
# The Controller/MultiEngine side of things
#-------------------------------------------------------------------------------
def strToShape(s):
    l = s[1:-1].replace(' ','').split(',')
    # print l
    if l[-1] == '':
        l = l[:-1]
    return tuple(map(int, l))

def serialize(obj):
    serial = newserialized.serialize(obj)
    data = serial.getData()
    typeDescriptor = serial.getTypeDescriptor()
    md = serial.getMetadata()
    headers = {'serial-type': typeDescriptor}
    if typeDescriptor == 'ndarray':
        # pass
        headers['dtype'] = md['dtype']
        headers['shape'] = str(md['shape'])
    headers = prefixHeaders(headers)
    # print headers
    return headers, data

def unserialize(headers, data):
    # print headers, data
    h = getPrefixedHeaders(headers)
    typeDescriptor = h['serial-type']
    md = {}
    if typeDescriptor == 'pickle':
        pass
    elif typeDescriptor == 'ndarray':
        md['dtype'] = h['dtype']
        md['shape'] = strToShape(h['shape'])
    serial = newserialized.Serialized(data, typeDescriptor, md)
    return newserialized.unserialize(serial)
    
def prefixHeaders(dikt, prefix='x-ipy-'):
    newDikt = {}
    for k, v in dikt.iteritems():
        newDikt[prefix + k] = v
    return newDikt

def getPrefixedHeaders(dikt, prefix='x-ipy-'):
    newDikt = {}
    n = len(prefix)
    for k,v in dikt.iteritems():
        if k[:n] == prefix:
            newDikt[k[n:]] = dikt[k]
    return newDikt

def htmlTargetString(targets):
    if targets == 'all':
        return targets
    elif isinstance(targets, (tuple, list)):
        return ','.join(map(str, targets))
    elif isinstance(targets, int):
        return str(targets)
    raise error.InvalidEngineID(str(targets))

def htmlArgString(dikt):
    s = '?'
    for k,v in dikt.iteritems():
        if isinstance(v, str):
            vs = v
        elif isinstance(v, bool):
            if v:
                vs = '1'
            else:
                vs = '0'
        elif isinstance(v, (int, float, type(None))):
            vs = str(v)
        else:
            vs = pickle.dumps(v,2)
        s += k+'='+vs+'&'
    return s[:-1]

def strDict(dikt):
    d = {}
    for k,v in dikt.iteritems():
        if isinstance(v, str):
            vs = v
        elif isinstance(v, bool):
            if v:
                vs = '1'
            else:
                vs = '0'
        elif isinstance(v, (int, float, type(None))):
            vs = str(v)
        else:
            vs = pickle.dumps(v,2)
        d[k] = vs
    return d


