Ten-second overview:

File mycontroller.py:
---------------
from solariwsgi import this, DispatchTarget, controller

@DispatchTarget('myproj.hello', '/hello/{name}', name='.*')
@controller
def hello(name):
    return "Hello {}!".format(name)
---------------

File run.py:
------------
import solariwsgi
import mycontroller

from wsgiref.simple_server import make_server

make_server('127.0.0.1', 8080, solari.application).serve_forever()
------------

$ python run.py

And that's enough to be off to the races with!  Of course, there's more to it
than that.  If you set up the myproj package like:

./myproj/
    __init__.py
    controllers/
        __init__.py  # Content: import mycontroller
        mycontroller.py
    static/
        js/
            myjavascript.js
    templates/
        mygenshi.xml

File mycontroller.py:
---------------
from solariwsgi import this, DispatchTarget, controller

@DispatchTarget('myproj.hello', '/hello/{name}', name='.*')
@controller
def hello(name):
    return this.render('myproj/mygenshi.xml', {name=name, title='hello'})
---------------

File mygenshi.xml:
------------------
<html>
    <head>
        <title>${title}</title>
        <script type="text/javascript" href="${urlfor('static', package='myproj', path='js/myjavascript.js')}"/>
    </head>
    <body>
        Hello, ${name}!
    </body>
</html>
------------------

File run.py:
------------
import solariwsgi
import solariwsgi.controllers.static

solariwsgi.registerPackage('myproj')

from wsgiref.simple_server import make_server

make_server('127.0.0.1', 8080, solari.application).serve_forever()
------------

Here's the magic that's going on:

- importing solariwsgi.controllers.static sets up a controller for static content.
- registerPackage imports myproj.controllers (which in turn imports mycontroller).
- urlfor is a function that takes a dispatch target name and kwargs and makes a URL to that target.
- this and urlfor get added to the namespace used for rendering genshi templates.
