
import os
import sys
import site

site.addsitedir('/path/to/dmirr/git/src/dmirr.hub/')
site.addsitedir('/path/to/dmirr/env/lib/python2.6/site-packages/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'dmirr.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()