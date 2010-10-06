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
import json
import pprint
import string

# 3rd party packages

# in-house
try:
    from solariwsgi import context
except ImportError:
    context = None



def ajaxify(controller):
    def ajaxify_(*args, **kwargs):
        context.ajaxdata_ = []

        ret = controller(*args, **kwargs)

        assert ret is None

        context.response.content_type = 'application/json'
        return json.dumps(context.ajaxdata_)
    return ajaxify_


def append(selector, html, data_=None):
    """
    >>> data_ = []
    >>> append('#foo', '<b>foo</b>', data_)
    >>> pprint.pprint(data_)
    [{'action': 'append', 'html': '<b>foo</b>', 'selector': '#foo'}]
    """

    if data_ is None:
        data_ = context.ajaxdata_
    data_.append({'action':'append', 'selector':selector, 'html':html})

def jseval(script, data_=None, **kwargs):
    """
    >>> data_ = []
    >>> jseval('var foo = 1;', data_)
    >>> pprint.pprint(data_)
    [{'action': 'eval', 'script': 'var foo = 1;'}]
    """
    if data_ is None:
        data_ = context.ajaxdata_

    if kwargs:
        script = string.Template(script).substitute(kwargs)

    data_.append({'action':'eval', 'script':script})

def content(selector, html, anim='instant', data_=None):
    """
    >>> data_ = []
    >>> content('#foo', '<b>foo</b>', data_=data_)
    >>> pprint.pprint(data_)
    [{'action': 'content', 'anim': 'instant', 'html': '<b>foo</b>', 'selector': '#foo'}]
    """
    if data_ is None:
        data_ = context.ajaxdata_
    data_.append({'action':'content', 'selector':selector, 'html':html, 'anim':anim})

def replace(selector, html, anim='instant', data_=None):
    """
    >>> data_ = []
    >>> replace('#foo', '<b>foo</b>', data_=data_)
    >>> pprint.pprint(data_)
    [{'action': 'replace', 'anim': 'instant', 'html': '<b>foo</b>', 'selector': '#foo'}]
    """
    if data_ is None:
        data_ = context.ajaxdata_
    data_.append({'action':'replace', 'selector':selector, 'html':html, 'anim':anim})


#eof
