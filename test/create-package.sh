#!/bin/bash
set -e

rm -rf build
rm -rf dist
rm -rf kipartman.egg-info

python setup.py sdist bdist_wheel
twine register dist/kipartman-*.tar.gz
twine upload dist/*