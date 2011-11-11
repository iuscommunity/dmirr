import os, sys, site
sys.stdout = sys.stderr
 
os.environ['PYTHON_EGG_CACHE'] = '/var/www/vhosts/dmirr.example.com/python-egg-cache'
site.addsitedir('/var/www/vhosts/dmirr.example.com/dmirr-env/lib64/python2.6/site-packages')
 
sys.path.insert(0, '/var/www/vhosts/dmirr.example.com/dmirr/')
 
from paste.deploy import loadapp
application = loadapp('config:/var/www/vhosts/dmirr.example.com/dmirr/prod.ini')
