"""dMirr core exceptions module."""

class dMirrError(Exception):
    """Generic errors."""
    def __init__(self, value, code=1):
        Exception.__init__(self)
        self.msg = value
        self.code = code
    
    def __str__(self):
        return self.msg
    
    def __unicode__(self):
        return str(self.msg)
            
class dMirrConfigError(dMirrError):
    """Config parsing and setup errors."""
    def __init__(self, value):
        code = 1010
        dMirrError.__init__(self, value, code)

class dMirrRuntimeError(dMirrError):
    """Runtime errors."""
    def __init__(self, value):
        code = 1020
        dMirrError.__init__(self, value, code)
        
class dMirrArgumentError(dMirrError):
    """Argument errors."""
    def __init__(self, value):
        code = 1030
        dMirrError.__init__(self, value, code)

class dMirrInterfaceError(dMirrError):
    """Interface errors."""
    def __init__(self, value):
        code = 1040
        dMirrError.__init__(self, value, code)