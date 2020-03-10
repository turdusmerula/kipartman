#!/usr/bin/env python
# coding=utf-8

#
# To publish package release
# python setup.py sdist upload -r pypi
#

from __future__ import absolute_import
from __future__ import print_function

import io
from os.path import dirname
from os.path import join
from setuptools import setup, find_packages
from glob import glob

def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')).read()

setup(
    name='kipartman',
    version='0.6.2',
    description='Kicad part manager',
#     long_description='%s\n%s' %
#     (re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub(
#         '', read('README.rst')),
#      re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))),
    url='https://github.com/turdusmerula/kipartman/',
    author='Sebastien Besombes',
    license='GPLv3',

    scripts=['kipartman/__main__.py'],
    packages=find_packages('.'),
    package_dir={'': '.'},
    package_data={
        'kipartman.resources': ['*.png'], 
        'kipartbase.swagger_server.swagger': ['*.yaml'],
        },
#    data_files=[('kipartman.resources' , glob('kipartman/resources/*.png')),],
#    data_files=[('images' , glob('kipartman/resources/*.png')),],
#    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'kipartman = kipartman.__main__:main',
            'kipartbase = kipartbase.__main__:main',
        ]
    },

    install_requires=[
         'wxPython',
         'cfscrape',
         'docutils',
         'asyncio',
         'pathlib2',
         'pycairo',
         'conan',
         'pyrfc3339',
#         # for kipart base
         'connexion',
         'python_dateutil',
         'django',
         'django-mptt',
         'watchdog',
         'numpy',
         'sqlalchemy',
         'setuptools',
         'werkzeug==0.16.1',
         'connexion[swagger-ui]',
         'profiling'
    ],
)

