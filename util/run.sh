
CLEAN=0
if [ "$1" == "clean" ]; then
    CLEAN=1
fi

if [ ! -e './src' ]; then
    echo "You're not running out of the dmirr root dir."
    exit 1
fi

source ~/env/dmirr/bin/activate

pushd ./src/dmirr.hub/
    python setup.py develop
    if [ -e './dmirr_dev.db' ]; then
        if [ "$CLEAN" == "1" ]; then
            rm ./dmirr_dev.db
        fi
    fi
    echo 'no' | python dmirr/hub/manage.py syncdb
    python dmirr/hub/manage.py check_permissions
    python dmirr/hub/manage.py runserver
popd