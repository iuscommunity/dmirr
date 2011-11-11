# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='dMirr',
    version='0.5',
    description='Distributed Mirror Server Manager',
    author='BJ Dierkes',
    author_email='wdierkes@rackspace.com',
    url='http://github.com/derks/dmirr',
    install_requires=[
        "TurboGears2==2.0.3",
        "TurboMail >=3.0b2",
        "tg.devtools < 2.1",
        # "MySQLdb", if you want to use MySQL backend
        "pygeoip",
        "geopy",
        "BeautifulSoup",
        "pydns",
        "Babel >=0.9.4",
        "toscawidgets >= 0.9.7.1",
        "tw.forms",
        "zope.sqlalchemy >= 0.4",
        "repoze.tm2 >= 1.0a4",
        "repoze.what_quickstart >= 1.0",
        ],
    setup_requires=["PasteScript >= 1.7"],
    paster_plugins=['PasteScript', 'Pylons', 'TurboGears2', 'tg.devtools'],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['WebTest', 'BeautifulSoup'],
    package_data={'dmirr': ['i18n/*/LC_MESSAGES/*.mo',
                               'templates/*/*',
                               'public/*/*']},
    message_extractors={'dmirr': [
            ('**.py', 'python', None),
            ('templates/**.mako', 'mako', None),
            ('templates/**.html', 'genshi', None),
            ('public/**', 'ignore', None)]},

    entry_points="""
    [paste.app_factory]
    main = dmirr.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
    namespace_packages=['dmirr'],
)
