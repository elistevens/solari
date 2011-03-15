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
import os
import subprocess
import time
import unittest

# 3rd party packages
from selenium import selenium

# in-house
import solariwsgi
import solariwsgi._webapp.static
import solariwsgi._webapp.helloworld

from solariwsgi.testing.test_selenium import TestCaseSeleniumBase

server_code = '''
import sys
from wsgiref.simple_server import make_server
import solariwsgi
for p in sys.argv[1:]:
    solariwsgi.registerPackage(p)
wsgi_server = make_server('127.0.0.1', 8080, solariwsgi.application)
try:
    wsgi_server.serve_forever()
except Exception, e:
    print >>file('/tmp/server_error.log', 'w'), type(e), e
    raise
'''

class TestBasic(TestCaseSeleniumBase):
    solariPackages = ['solariajax', 'solariajax._webapp.testing']

    def setUp(self):
        self.selWarnings = []

    def test_replace(self):
        sel = self.selenium
        sel.open("/_test/basic")
        sel.wait_for_page_to_load(1000)

        self.selAssert(True, 'is_text_present', "before replace")

    #@unittest.expectedFailure
    #def test_helloworld_aaa(self):
    #    sel = self.selenium
    #    sel.open("/helloworld")
    #    sel.wait_for_page_to_load(1000)
    #
    #    self.selWarning(True, 'is_text_present', "hello world aaa")
    #    self.selWarning(True, 'is_text_present', "hello world ccc")
    #
    #    self.assertEqual([], self.selWarnings)
    #
    #@unittest.expectedFailure
    #def test_helloworld_xxx(self):
    #    sel = self.selenium
    #    sel.open("/helloworld")
    #    sel.wait_for_page_to_load(1000)
    #
    #    self.selAssert(True, 'is_text_present', "hello world xxx")

    def tearDown(self):
        pass





if __name__ == "__main__":
    unittest.main()
