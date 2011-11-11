# -*- coding: utf-8 -*-

class dMirrError(Exception):
    def __init__(self, msg):
        self.msg = msg

class dMirrArgumentError(dMirrError):
    def __init__(self, msg):
        Error.__init__(self, msg)

class dMirrError(dMirrError):
    def __init__(self, msg):
        Error.__init__(self, msg)