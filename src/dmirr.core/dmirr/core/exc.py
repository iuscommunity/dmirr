"""dMirr core exceptions module."""

class dMirrError(Exception):
    """Generic errors."""
    def __init__(self, msg):
        super(dMirrError, self).__init__()
        self.msg = msg
    
    def __repr__(self):
        return "dMirrError: %s" % self.msg
        
    def __str__(self):
        return self.msg
            
class dMirrConfigError(dMirrError):
    """Config parsing and setup errors."""
    def __init__(self, ):
        super(dMirrConfigError, self).__init__(msg)

class dMirrRuntimeError(dMirrError):
    """Runtime errors."""
    def __init__(self, msg):
        super(dMirrError, self).__init__(msg)
        
class dMirrArgumentError(dMirrError):
    """Argument errors."""
    def __init__(self, msg):
        super(dMirrArgumentError, self).__init__(msg)

class dMirrAPIError(dMirrError):
    """API connection errors."""
    def __init__(self, msg):
        super(dMirrAPIError, self).__init__(msg)