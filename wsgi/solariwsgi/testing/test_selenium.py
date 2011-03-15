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
#
# Originally based off of test cases made by Selenium IDE; very little of that
# remains.

# stdlib
#import copy
#import doctest
#import gc
#import random
#import sys
#import time
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

class TestCaseSeleniumBase(unittest.TestCase):

    seleniumHost = 'localhost'
    seleniumPort = '4444'
    seleniumBrowser = os.environ.get('SELENUIM_BROWSER', "*firefox3 /Applications/Firefox3.app/Contents/MacOS/firefox-bin")
    seleniumAppURL = "http://localhost:8080"

    solariPackages = []


    @classmethod
    def setUpClass(cls):
        cls.wsgi_server = subprocess.Popen(['python', '-c', server_code] + (cls.solariPackages if cls.solariPackages else ['solariwsgi._webapp.helloworld']))

        cls.seleniumRC = subprocess.Popen(['java', '-jar', 'selenium-server-standalone-2.0a4.jar'])

        for i in range(100):
            try:
                cls.selenium = selenium(cls.seleniumHost, cls.seleniumPort, cls.seleniumBrowser, cls.seleniumAppURL)
                cls.selenium.start()
            except Exception, e:
                time.sleep(0.1)
            else:
                break

    @classmethod
    def tearDownClass(cls):
        cls.wsgi_server.terminate()
        cls.wsgi_server.wait()

        ## This seems required to make sure that the page gets written, otherwise
        ## the server complains.  :-/
        #time.sleep(1)
        cls.selenium.stop()

        cls.seleniumRC.terminate()
        cls.seleniumRC.wait()


    def selAssert(self, result, func, *args):
        self.assertEquals(result, getattr(self.selenium, func)(*args), 'Error: sel.{}({}) != {!r}'.format(func, ', '.join([repr(x) for x in args]), result))

    def selWarning(self, result, func, *args):
        try:
            self.assertEquals(result, getattr(self.selenium, func)(*args), 'Warning: sel.{}({}) != {!r}'.format(func, ', '.join([repr(x) for x in args]), result))
        except Exception, e:
            self.selWarnings.append(e)


    def setUp(self):
        self.selWarnings = []

    def test_helloworld_pass(self):
        sel = self.selenium
        sel.open("/helloworld")
        sel.wait_for_page_to_load(1000)

        self.selAssert(True, 'is_text_present', "hello world")

    @unittest.expectedFailure
    def test_helloworld_aaa(self):
        sel = self.selenium
        sel.open("/helloworld")
        sel.wait_for_page_to_load(1000)

        self.selWarning(True, 'is_text_present', "hello world aaa")
        self.selWarning(True, 'is_text_present', "hello world ccc")

        self.assertEqual([], self.selWarnings)

    @unittest.expectedFailure
    def test_helloworld_xxx(self):
        sel = self.selenium
        sel.open("/helloworld")
        sel.wait_for_page_to_load(1000)

        self.selAssert(True, 'is_text_present', "hello world xxx")

    def tearDown(self):
        pass





if __name__ == "__main__":
    unittest.main()
