#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from tornado.util import import_object

from . import default


class Setting():
    def __init__(self, settings_module=None):
        for setting in dir(default):
            if setting == setting.upper():
                setattr(self, setting, getattr(default, setting))

        if settings_module:
            self.load(settings_module)

    def load(self, settings_module):
        try:
            mod = import_object(settings_module)
        except ImportError as e:
            raise ImportError('Could not import setting module %s: %s' % (settings_module, e))

        for setting in dir(mod):
            if setting == setting.upper():
                setattr(self, setting, getattr(mod, setting))

    def configure(self, setting, value):
        setattr(self, setting, value)


setting = Setting()


try:
    setting.load(os.environ['NWB_SETTING'])
except KeyError:
    pass

