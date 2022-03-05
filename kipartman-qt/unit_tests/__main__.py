#!/bin/python3

import os
import unittest 
import sys

# os.sys.path.append(os.path.dirname(os.path.abspath(__file__)))
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
xpl_path = os.path.abspath(os.path.dirname(__file__))
os.chdir(base_path)
sys.path.append(base_path)
sys.path.append(xpl_path)


# test api
# from test_ndict import *
from test_unit import *

if __name__ == '__main__':
    unittest.main(verbosity=2)
