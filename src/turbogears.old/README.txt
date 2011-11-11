NAME: dMirr

CREATOR: BJ Dierkes <wdierkes@rackspace.com>

DESCRIPTION:

dMirr is a distributed mirror server manager. It's purpose is to organize data 
for upstream projects needing global mirror servers, and the generous sites 
willing to help mirror those projects.

Features Include:

    * Yum "mirror list" interface. Closest match ordered via geoip location
    * RESTful web framework using Apache, WSGI, and TurboGears 2


Support

    * http://github.com/derks/dmirr/issues

LICENSING

dMirr is Open Source and is distributed under the GNU GPL v2.  See the 
LICENSE file included with this software.


INSTALLATION:

The ./util/init_project.py can be used to setup a Python virtualenv and the 
initial setup for development (sqlite database + data).

    $ cd dmirr
    $ bash ./util/init_project.sh

Start the paste http server::

    $ paster serve --reload dev.ini

Then you are ready to go.

