#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tornado.escape import to_unicode


def T(value):
    if value is None:
        raise ValueError
    return value


def flatten_arguments(args):
    flattened = {}
    for key in args:
        if len(args[key]) == 1:
            flattened[key] = to_unicode(args[key][0])
        else:
            flattened[key] = (to_unicode(arg) for arg in args[key])
    return flattened

