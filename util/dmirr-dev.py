#!/usr/bin/env python

import os
import sys
from subprocess import Popen, PIPE
from cement2.core import foundation, handler, controller
 
app = foundation.lay_cement('dmirr_dev')

BASE = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PKGS = [
    'dmirr.core',
    'dmirr.cli',
    'dmirr.hub',
    ]
    
class BaseController(controller.CementBaseController):
    class Meta:
        label = 'base'
        description = 'dMirr Development Utilities'
        arguments = [
            (['package'], dict(action='store', 
                               nargs='?', 
                               help='a dmirr source package')),
            (['--clean'], dict(action='store_true',  
                               help='clean/reinstall files')),
            ]
            
    def _exec(self, cmd_args):
        self.log.debug( "Executing: %s" % ' '.join(cmd_args) )
        proc = Popen(cmd_args, stdout=PIPE, stderr=PIPE)
        (stdout, stderr) = proc.communicate()
        if app.config.get('base', 'debug'):
            print stdout
        proc.wait()
        return (stdout, stderr, proc.returncode)
        
    def _setup_package(self, package):
        orig_dir = os.curdir
        os.chdir("%s/src/%s" % (BASE, package))
        ret = 0    
        if os.path.exists('./requirements.txt'):
            out, err, ret = self._exec(
                ['pip', 'install', '--requirement=requirements.txt']
                )
        out, err, ret2 = self._exec(['python', 'setup.py', 'develop'])
        
        ret_total = ret + ret2
        if ret_total != 0:
            self.log.fatal("Installing: %s" % package)
        else:
            self.log.info("Installed: %s" % package)
            
        os.chdir(orig_dir)
        
    @controller.expose(help='setup and install requirements')
    def setup(self):
        if self.pargs.package == 'all':
            for pkg in PKGS:
                self._setup_package(pkg)
        elif self.pargs.package not in PKGS:
            raise Exception('src/%s does not exist' % self.pargs.package)
        else:
            self._setup_package(self.pargs.package)
    
    @controller.expose(help='run dmirr.hub service')
    def run(self):
        os.chdir("%s/src/dmirr.hub" % BASE)
        if self.pargs.clean:
            if os.path.exists('dmirr_dev.db'):
                os.remove('dmirr_dev.db')
            os.system("echo 'no' | python dmirr/hub/manage.py syncdb")
            os.system("DJANGO_SETTINGS_MODULE=dmirr.hub.settings django-admin.py loaddata dmirr/hub/fixtures/test_data.yaml")
        os.system('python dmirr/hub/manage.py check_permissions')
        os.system('python dmirr/hub/manage.py runserver 0.0.0.0:8001')
            
        
        
    
                
handler.register(BaseController)        

try:
    if 'VIRTUAL_ENV' not in os.environ:
        raise Exception('Not working within a virtualenv!')
    
    app.setup()
    app.run()
except Exception as e:
    print "Exception: %s" % e.args[0]
    sys.exit(1)
finally:
    app.close()