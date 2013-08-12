#!/usr/bin/python

import inspect


def caller():
    return inspect.stack()[2][3]


def print_debug(msg, tag = None):
    if tag:
        print '[%s][%s] %s' % (caller(), tag, msg)
    else:
        print '[%s] %s' % (caller(), msg)
