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


#import collections
import copy
import datetime
import functools
import itertools
#import os, os.path
import re
#import threading
import urllib

import markdown

class _Base(object):
    def __init__(self):#, **kwargs):
        pass
        #self.defaults(**kwargs)

    def defaults(self, onclear_='reuse', **kwargs):
        if onclear_ == 'copy':
            self.copyDefaults_dict.update(kwargs)
        else:
            self.reuseDefaults_dict.update(kwargs)

    def reset(self):
        self.__dict__.clear()
        self.__dict__.update({k: globals()[k] for k in self.globalDefaults_list})
        self.__dict__.update(self.reuseDefaults_dict)
        self.__dict__.update(copy.deepcopy(self.copyDefaults_dict))

        #print "reset: copy ", type(self), self.copyDefaults_dict
        #print "reset: reuse", type(self), self.reuseDefaults_dict
        #print "reset: dict ", type(self), self.__dict__



class Context(_Base):
    globalDefaults_list = []
    reuseDefaults_dict = {}
    copyDefaults_dict = {}

    def reset(self):
        _Base.reset(self)
        self.tmpl = tmpl

class Tmpl(_Base):
    globalDefaults_list = ['copy', 'datetime', 'functools', 'itertools', 're', 'urllib', 'markdown']
    reuseDefaults_dict = {}
    copyDefaults_dict = {}

    def reset(self):
        _Base.reset(self)
        self.context = context

context = Context()
tmpl = Tmpl()

context.reset()
tmpl.reset()

# eof
