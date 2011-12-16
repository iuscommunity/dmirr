
from cement2.core import backend, foundation
from cement2.core import exc as cement_exc

from dmirr.core import exc

def main():
    defaults = backend.defaults('dmirr')
    defaults['base']['hub_baseurl'] = 'http://dmirr.example.com'
    defaults['base']['hub_api_user'] = 'nobody'
    defaults['base']['hub_api_key'] = ''
    app = foundation.lay_cement('dmirr', defaults=defaults)
    
    from dmirr.cli.bootstrap import base
    
    app.setup()
        
    try:
        app.run()
    except cement_exc.CementRuntimeError as e:
        print "dMirrRuntimeError => %s" % e.msg
    except exc.dMirrRuntimeError as e:
        print "dMirrRuntimeError => %s" % e.msg
    except cement_exc.CementArgumentError as e:
        print "dMirrArgumentError => %s" % e.msg
    except exc.dMirrArgumentError as e:
        print "dMirrArgumentError => %s" % e.msg
    finally:
        app.close()

if __name__ == '__main__':
    main()