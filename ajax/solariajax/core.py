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

# 3rd party packages

# in-house
try:
    from solariwsgi import context
except ImportError:
    class This(object):
        pass
    
    this = This()

def ajaxify(controller):
    def ajaxify_(*args, **kwargs):
        context.ajax_data = []
        
        ret = controller(*args, **kwargs)
        
        assert ret is None
        
        context.response.content_type = 'application/json'
        return json.dumps(context.ajax_data)
    return ajaxify_


def append(selector, html):
    context.ajax_data.append({'action':'append', 'selector':selector, 'html':html})

def jseval(script):
    context.ajax_data.append({'action':'eval', 'script':script})

def replace(selector, html):
    context.ajax_data.append({'action':'replace', 'selector':selector, 'html':html})


#eof
