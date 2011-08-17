#!/bin/bash
#
# should be run as
#
# $ bash ./util/init_devel.sh
# 

cwd=$(pwd)
tmp=$(mktemp -t /tmp -d)
uid=$(id -u -nr)
cd $tmp

mkdir -p ~/devel/env

virtualenv --no-site-packages ~/devel/env/dmirr

source ~/devel/env/dmirr/bin/activate
easy_install ez-setup
easy_install -i http://www.turbogears.org/2.0/downloads/current/index tg.devtools

python setup.py develop
cp -a dev.ini-example dev.ini
paster setup-app dev.ini

clear

cat <<EOF
dMirr Development Quickstart Complete.  Now edit your config file
at ${cwd}/dev.ini and then run:

$ source ~/devel/env/dmirr/bin/activate

$ paster serve --reload dev.ini

EOF
