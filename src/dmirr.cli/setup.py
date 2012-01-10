
from setuptools import setup, find_packages
import sys, os

VERSION = '1.9.1'

setup(name='dmirr.cli',
    version=VERSION,
    description="dMirr Command Line Interface",
    long_description="dMirr Command Line Interface",
    classifiers=[], 
    keywords='',
    author='BJ Dierkes',
    author_email='wdierkes@rackspace.com',
    url='http://github.com/rackspace/dmirr',
    license='GPLv2',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=[
        "cement2 >= 1.9.3",
        "cement2.ext.genshi >= 1.9.5",
        ### Required for testing
        # "nose",
        # "coverage",
        ],
    setup_requires=[
        ],
    entry_points="""
    [console_scripts]
    dmirr = dmirr.cli.appmain:main
    """,
    namespace_packages=[
        'dmirr',
        'dmirr.cli',
        ],
    )
