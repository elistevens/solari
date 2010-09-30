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

# stdlib
import collections
import copy
import datetime
import functools
import itertools
import os, os.path
import re
import threading
import urllib

# 3rd party packages
import pkg_resources

import webob
from webob import Request, Response
#from webob import exc

# in-house
from contextobj import context, tmpl


def application(environ, start_response):
    context.reset()
    tmpl.reset()

    context.request = Request(environ)
    #context.response = Response(charset='utf8')
    context.response = Response()
    context.now = datetime.datetime.now()

    request_url = context.request.path_info.split('?', 1)[0]

    for target in DispatchTarget.target_dict.values():
        match = target.regex.match(request_url)

        #print "match:", match, target.name, target, repr(context.request.path_info)
        if match:
            environ['URLVAR'] = context.urlvar_dict = match.groupdict()
            environ['URLFOR'] = context.urlfor = functools.partial(urlfor, **match.groupdict())

            #print type(environ['URLVAR']), repr(environ['URLVAR'])

            try:
                return target.app(environ, start_response)
            finally:
                pass
                #print "Context:", sorted(context.__dict__)
                #print "Tmpl:   ", sorted(tmpl.__dict__), tmpl.reuseDefaults_dict

    # FIXME: 404
    start_response('404 Not Found', [('Content-type', 'text/plain')])
    return [str(x) + '\n' for x in sorted(environ.items())] + [str(x) + '\n' for x in DispatchTarget.target_dict]


_packageCallback_list = []
def packageCallback(callback):
    _packageCallback_list.append(callback)
    return callback

@packageCallback
def packageCallback_importControllers(packagename):
    try:
        __import__('{}.controllers'.format(packagename))
    except ImportError, e:
        print e
        #raise
        pass

def registerPackage(packagename):
    for callback in _packageCallback_list:
        callback(packagename)


class DispatchTarget(object):
    target_dict = collections.OrderedDict()
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
        self.regex = re.compile('^' + pattern_.format(**format_kwargs) + ('/?$' if slash_ else '$'))

        print name_, '^' + pattern_.format(**format_kwargs) + ('/?$' if slash_ else '$')

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


def controller(app):
    def middleware_controller(environ, start_response):
        try:
            body = app(**context.urlvar_dict)

            #print repr(body)

        #except webob.exc.HTTPException, e:
        #    # ???
        #    context.response = e
        except:
            print context.request
            raise
        finally:
            pass

        if isinstance(body, basestring):
            context.response.body = body
        else:
            context.response.app_iter = iter(body)

        return context.response(environ, start_response)

    return middleware_controller


def urlfor(name_, params=None, anchor=None, **kwargs):
    target = DispatchTarget.target_dict[name_]

    urlvar_dict = {}
    urlvar_dict.update(context.urlvar_dict)
    urlvar_dict.update(kwargs)

    url_str = target.pattern.format(**urlvar_dict)
    assert target.regex.match(url_str), '{} vs. {}'.format(target.pattern, url_str)

    params = ('?' + urllib.urlencode(params)) if params else ''
    #base_str = '' if target.root else context.request.script_name
    base_str = context.request.script_name

    if isinstance(anchor, basestring):
        anchor = '#' + anchor
    else:
        anchor = ('#' + urllib.urlencode(anchor)) if anchor else ''

    return base_str + url_str + params + anchor



tmpl.defaults(urlfor=urlfor)

# This eventually needs to get split out into its own package...

#from solariwsgi.core import packageCallback, this

from genshi.template import TemplateLoader, loader
from genshi.template.text import NewTextTemplate
_loader_dict = {}



@packageCallback
def packageCallback_genshisolari(packagename):
    #print "packageCallback_genshisolari"
    _loader_dict[packagename] = loader.package(packagename, 'templates')

    templateLoader = TemplateLoader(loader.prefixed(**_loader_dict), max_cache_size=100*len(_loader_dict))

    def generate_tmpl(template_path, data=None, cls=None):
        render_dict = {}

        if tmpl.__dict__:
            render_dict.update(tmpl.__dict__)

        if data:
            render_dict.update(data)

        return templateLoader.load(template_path, cls=cls).generate(**render_dict)

    def text(template_path, data=None, method='text'):
        return generate_tmpl(template_path, data, NewTextTemplate).render(method)

    def render(template_path, data=None, method='xhtml'):
        return generate_tmpl(template_path, data).render(method)

    def serialize(template_path, data=None, method='xhtml'):
        return generate_tmpl(template_path, data).serialize(method)

    context.defaults(
            templateLoader = templateLoader,
            text = text,
            render = render,
            serialize  = serialize,
        )


def evenodd(iter, start=0):
    eo_list = ['even', 'odd']
    for i, x in enumerate(iter):
        i += start
        yield i, eo_list[i & 1], x

tmpl.defaults('reuse', evenodd=evenodd)





# eof
