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
import copy
import datetime
import doctest
import gc
import random
import re
import sys
import time
import unittest

# 3rd party packages
#import couchdb

# in-house
import solariajax


class TestPyApi(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_docs(self):
        # doctest returns a tuple of (failed, attempted)
        self.assertEqual(doctest.testmod(solariajax.core,
                optionflags=(doctest.REPORT_CDIFF | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS))[0], 0)


    def test_simple(self):
        pass

# eof
