"""
Copyright 2006 ThoughtWorks, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


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
import solariwsgi.controllers.static
import solariwsgi.controllers.helloworld

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
        cls.wsgi_server = subprocess.Popen(['python', '-c', server_code] + (cls.solariPackages if cls.solariPackages else ['solariwsgi.controllers.helloworld']))

        cls.seleniumRC = subprocess.Popen(['java', '-jar', 'selenium-server.jar'])

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
