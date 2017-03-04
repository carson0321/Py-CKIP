#!/usr/bin/python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: tests.py
# Author: Carson Wang
# mail: kiki86151@hotmail.com
# Created Time: 2017-03-04 21:41:52
#########################################################################

from __future__ import unicode_literals, print_function
from PyCKIP import *


def traverse(root):
    #Helper function to traverse all leaf nodes of the given tree root.
    if 'child' in root:
        for child in root['child']:
            for leaf in traverse(child):
                yield leaf
    else:
        yield root


# Usage example of the CKIPSegmenter class
segmenter = PyCKIP.CKIPSegmenter('YOUR USERNAME', 'YOUR PASSWORD')
result = segmenter.process('這是一隻可愛的小花貓')
if result['status_code'] != '0':
    print('Process Failure: ' + result['status'])

for sentence in result['result']:
    for term in sentence:
        print(term['term'], term['pos'])


# Usage example of the CKIPParser class
parser = PyCKIP.CKIPParser('YOUR USERNAME', 'YOUR PASSWORD')
result = parser.process('這是一隻可愛的小花貓')
if result['status_code'] != '0':
    print('Process Failure: ' + result['status'])

for sentence in result['result']:
    for term in traverse(sentence['tree']):
        print(term['term'], term['pos'])

