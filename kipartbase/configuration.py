from os.path import expanduser
import os.path
import json
import logging, sys
import platform
from distutils.spawn import find_executable

class Configuration(object):
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.expanduser("~"), '.kipartman')
        self.storage_path = os.path.join(self.data_dir, 'storage')
        self.version_storage_path = os.path.join(self.data_dir, 'version_storage')
        self.sub_levels = 3
        self.sub_level_size = 2
        
    def set_data_dir(self, value):
        self.data_dir = value
        self.storage_path = os.path.join(self.data_dir, 'storage')
        self.version_storage_path = os.path.join(self.data_dir, 'version_storage')
        
configuration=Configuration()
