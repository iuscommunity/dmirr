
from setuptools import setup, find_packages
import sys, os

VERSION = '1.9.1'

setup(name='dmirr.core',
    version=VERSION,
    description="dMirr Core",
    long_description="dMirr Core",
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
        ],
    setup_requires=[
        ],
    entry_points="""
    """,
    namespace_packages=[
        'dmirr',
        'dmirr.hub',
        'dmirr.cli',
        ],
    )
