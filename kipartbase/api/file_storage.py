import uuid
import shutil
import os
import api.models
import tempfile
import helper.hash as hash
from configuration import configuration

from django.conf import settings

from os.path import expanduser
home = expanduser("~")

class FileStorage(object):

    def __init__(self):
        self.storage_path = configuration.storage_path
        self.sub_levels = configuration.sub_levels
        self.sub_level_size = configuration.sub_level_size
    
    def get_sublevels(self, id):
        levels = []
        for level in range(self.sub_levels):
            start = level*self.sub_level_size
            stop = (level+1)*self.sub_level_size
            levels.append(id[start:stop])
        return levels

    def add_file(self, upfile):
        # get content
        file = tempfile.NamedTemporaryFile(delete=False)
        upfile.save(file)
        file.flush()
        file.close()
        
        # get md5
        md5 = hash.md5(file.name).hexdigest()
        levels = self.get_sublevels(md5)
        
        # get current sublevel
        storage_path = ''
        
        # create sublevels
        dir = self.storage_path
        for level in levels:
            dir = os.path.join(dir, level)
            storage_path = os.path.join(storage_path, level)
            if not os.path.exists(dir):
                os.makedirs(dir)
        dir = os.path.join(dir, md5)
        storage_path = os.path.join(storage_path, md5)
        if not os.path.exists(dir):
            os.makedirs(dir)
        storage_path = os.path.join(storage_path, upfile.filename)
        # copy file
        shutil.copyfile(file.name, os.path.join(dir, upfile.filename))
        #TODO: Delete file.name from temp storage

        # add file to db
        file = api.models.File(source_name=upfile.filename, storage_path=storage_path.replace('\\','/'))
        file.save()
        
        print("Add file", upfile.filename, "as", storage_path)
        return file
    
    def get_file(self, id):
        levels = self.get_sublevels(id)
        dir = self.storage_path
        for level in levels:
            dir = dir+"/"+level
        return dir+"/"+id
