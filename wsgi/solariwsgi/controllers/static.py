# Copyright (c) 2010 Eli Stevens
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import datetime
import os, os.path
import mimetypes

import pkg_resources

from solariwsgi import context, DispatchTarget, controller
from solariwsgi.core import packageCallback

_package_set = set()
@packageCallback
def packageCallback_static(packagename):
    _package_set.add(packagename)

@DispatchTarget('static', '/static/{package}/{path}', package='[a-zA-Z_]+', path='.+')
@controller
def static(package, path):
    if package in _package_set:
        
        content_type, content_encoding = mimetypes.guess_type(path)
        
        if content_type:
            context.response.content_type = content_type
        else:
            # FIXME: what to use by default?
            pass
        
        # FIXME: locale settings can mess this up.  see:
        # http://stackoverflow.com/questions/225086/rfc-1123-date-representation-in-python
        expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
        context.response.headers.add('Expires', expires.strftime("%a, %d %b %Y %H:%M:%S GMT"))
        
        return pkg_resources.resource_stream(package, os.path.join('static', path))

    else:
        return None
    

# eof
