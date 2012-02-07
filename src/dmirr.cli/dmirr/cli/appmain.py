
import os
import sys
import drest
from cement2.core import backend, foundation, handler, log
from cement2.core import exc as cement_exc
from cement2.lib.ext_logging import LoggingLogHandler

from dmirr.core import exc

defaults = backend.defaults('dmirr')
defaults['base']['extensions'].append('genshi')
defaults['base']['output_handler'] = 'genshi'
defaults['genshi'] = dict(
    template_module='dmirr.cli.templates',
    )
defaults['log'] = dict(
    file=None
    )
            
def main():
    app = foundation.lay_cement('dmirr', defaults=defaults)
    
    from dmirr.cli.bootstrap import base
    
    app.setup()
        
    try:
        app.run()
    except cement_exc.CementSignalError as e:
        pass
    except cement_exc.CementRuntimeError as e:
        print e
    except exc.dMirrRuntimeError as e:
        print e
    except cement_exc.CementArgumentError as e:
        print e
    except exc.dMirrArgumentError as e:
        print e
    except exc.dMirrAPIError as e:
        print e
    except drest.exc.dRestRequestError as e:
        print "dMirrAPIError => %s" % e.msg
    except drest.exc.dRestAPIError as e:
        print "dMirrAPIError => %s" % e.msg
    finally:
        app.close()

def test_main(argv=[]):
    import tempfile
    app = foundation.lay_cement('dmirr', defaults=defaults, argv=argv)
    
    from dmirr.cli.bootstrap import base
    
    app.setup()
    app.run()
        
if __name__ == '__main__':
    main()