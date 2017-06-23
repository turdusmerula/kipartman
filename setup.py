#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import
from __future__ import print_function

import io
from os.path import dirname
from os.path import join
from setuptools import setup, find_packages

def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')).read()

setup(
    name='kipartman',
    version='0.0.7',
    description='Kicad part manager',
#     long_description='%s\n%s' %
#     (re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub(
#         '', read('README.rst')),
#      re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))),
    url='https://github.com/turdusmerula/kipartman/',
    author='Sebastien Besombes',
    license='GPLv3',

    scripts=['src/kipartman.py'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
#    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'kipartman = kipartman:main'
        ]
    },

    install_requires=[
        'requests',
        'wxPython',
        'rfc3987',
        'cfscrape',
        'docutils'
    ],
)


