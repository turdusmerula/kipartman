#!/bin/bash
set -e

cd /

rm -rf /tmp/kipartman-testenv

virtualenv /tmp/kipartman-testenv
source /tmp/kipartman-testenv/bin/activate

#pip install kipartman --no-cache --no-deps
pip install kipartman

kipartman
