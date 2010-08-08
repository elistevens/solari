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


import functools
import os, os.path
import re
import threading
import urllib

import pkg_resources

import webob
from webob import Request, Response
#from webob import exc

this = threading.local()

#this.loader = lambda x: None

def application(environ, start_response):
    this.request = Request(environ)
    this.response = Response(charset='utf8')
    
    for target in DispatchTarget.target_dict:
        match = target.regex.match(this.request.path_info)
        
        if match:
            environ['URLVAR'] = this.urlvar_dict = match.groupdict()
            environ['URLFOR'] = this.urlfor = functools.partial(urlfor, **match.groupdict())
            
            return target.application(environ, start_response)
        
    # FIXME: 404
    start_response('404 Not Found', [('Content-type', 'text/plain')])
    return [str(x) + '\n' for x in sorted(environ.items())] + [str(x) + '\n' for x in DispatchTarget.target_dict]
    
#def registerController(*args, **kwargs):
#    AppUrl(*args, **kwargs)
    
# Might need to change sig to:
# def urlfor(name, urlparams={}, cgiparams={}, anchor,)
# or similar
def urlfor(name, params=None, anchor=None, **kwargs):
    target = DispatchTarget.target_dict[name]
    
    url_str = target.pattern.format(**kwargs)
    assert target.regex.match(url_str)
    
    params = ('?' + urllib.urlencode(params)) if params else ''
    #base_str = '' if target.root else this.request.script_name
    base_str = this.request.script_name
    
    if isinstance(anchor, basestring):
        anchor = '#' + anchor
    else:
        anchor = ('#' + urllib.urlencode(anchor)) if anchor else ''
    
    return base_str + url_str + params + anchor



def controller(app):
    def app_(environ, start_response):
        try:
            body = app(**this.urlvar_dict)
        #except webob.exc.HTTPException, e:
        #    # ???
        #    this.response = e
        finally:
            pass
        
        if isinstance(resp, basestring):
            this.response.body = body
        else:
            this.response.body_iter = iter(body)
            
        return this.response(environ, start_response)

    return app_


class DispatchTarget(object):
    target_dict = OrderedDict()
    ## FIXME: odict
    #appurl_list = []
    #appurl_dict = {}

    def __init__(self, name_, pattern_, app_=None, slash_=True, **kwargs):
        self.name = name_
        self.pattern = pattern_
        self.app = app_
        
        assert self.pattern.startswith('/')

        format_kwargs = {}
        for key, re_str in kwargs.items():
            format_kwargs[key] = r'(?P<%s>%s)' % (key, re_str)
        self.regex = re.compile(pattern_.format(**format_kwargs) + ('/?' if slash_ else ''))

        #self.appurl_list.append(self)
        self.target_dict[name_] = self
        
    def __repr__(self):
        return '<{0} object at {1}; {2}>'.format(
            self.__class__.__name__,
            hex(id(self)),
            ', '.join(['{0}={1}'.format(k, repr(v)) for k, v in sorted(self.__dict__.items())]))

    def __call__(self, app):
        """
        This allows the class instance to be used as a decorator.
        """
        self.setApplication(app)
        return self.app
        
    def setApplication(self, app):
        assert self.app is None
        self.app = app


@DispatchTarget('static', '/static/{package}/{filename}', package='[a-zA-Z_]+', filename='.+')
@controller
def static(package, filename):
    return pkg_resources.resource_string(package, os.path.join('static', filename))

# eof
