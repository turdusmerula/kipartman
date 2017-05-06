# #!/usr/bin/env python
# # coding=utf-8
# from __future__ import absolute_import
# from __future__ import print_function
# 
# from glob import glob
# import io
# from os.path import basename
# from os.path import dirname
# from os.path import join
# from os.path import splitext
# import re
# from setuptools import find_packages
# from setuptools import setup
# 
# 
# def read(*names, **kwargs):
#     return io.open(
#         join(dirname(__file__), *names),
#         encoding=kwargs.get('encoding', 'utf8')).read()
# 
# 
# setup(
#     name='kipartbase',
# 
#     # Versions should comply with PEP440.  For a discussion on single-sourcing
#     # the version across setup.py and the project code, see
#     # https://packaging.python.org/en/latest/single_source_version.html
#     version='0.0.1',
#     description='kipartbase',
#     long_description='%s\n%s' %
#     (re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub(
#         '', read('README.rst')),
#      re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))),
# 
#     # The project's main homepage.
#     url='https://github.com/turdusmerula/kipartman',
# 
#     # Author details
#     author='Sebastien Besombes',
#     author_email='sebastien.besombes@gmail.com',
# 
#     # Choose your license
#     license='GPLv3',
# 
#     # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
#     classifiers=[
#         # How mature is this project? Common values are
#         #   3 - Alpha
#         #   4 - Beta
#         #   5 - Production/Stable
#         'Development Status :: 3 - Alpha',
# 
#         # Indicate who your project is intended for
#         'Intended Audience :: Developers',
#         'Topic :: Software Development :: Build Tools',
# 
#         # Pick your license as you wish (should match "license" above)
#         'License :: OSI Approved :: {}'.format(license),
# 
#         # Specify the Python versions you support here. In particular, ensure
#         # that you indicate whether you support Python 2, Python 3 or both.
#         'Programming Language :: Python :: 2',
#         'Programming Language :: Python :: 2.7',
#         'Programming Language :: Python :: 3',
#         'Programming Language :: Python :: 3.3',
#         'Programming Language :: Python :: 3.4',
#         'Programming Language :: Python :: 3.5',
#     ],
# 
#     # What does your project relate to?
#     keywords='Kipart tools: development',
# 
#     # You can just specify the packages manually here if your project is
#     # simple. Or you can use find_packages().
#     packages=find_packages('.'),
#     package_dir={'': '.'},
#     # Alternatively, if you want to distribute just a my_module.py, uncomment
#     # this:
#     py_modules=[splitext(basename(path))[0] for path in glob('*.py')],
#     include_package_data=True,
# 
#     # List run-time dependencies here.  These will be installed by pip when
#     # your project is installed. For an analysis of "install_requires" vs pip's
#     # requirements files see:
#     # https://packaging.python.org/en/latest/requirements.html
#     install_requires=[
#         'django'
#     ],
# 
#     # List additional groups of dependencies here (e.g. development
#     # dependencies). You can install these using the following syntax,
#     # for example:
#     # $ pip install -e .[test]
#     extras_require={
#         'test': ['pytest'],
#     }, )
