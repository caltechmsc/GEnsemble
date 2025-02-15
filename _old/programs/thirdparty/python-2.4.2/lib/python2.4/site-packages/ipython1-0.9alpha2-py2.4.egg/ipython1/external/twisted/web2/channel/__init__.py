# -*- test-case-name: ipython1.external.twisted.web2.test.test_cgi,ipython1.external.twisted.web2.test.test_http -*-
# See LICENSE for details.

"""
Various backend channel implementations for web2.
"""
from ipython1.external.twisted.web2.channel.cgi import startCGI
from ipython1.external.twisted.web2.channel.scgi import SCGIFactory
from ipython1.external.twisted.web2.channel.http import HTTPFactory
from ipython1.external.twisted.web2.channel.fastcgi import FastCGIFactory

__all__ = ['startCGI', 'SCGIFactory', 'HTTPFactory', 'FastCGIFactory']
