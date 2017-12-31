from file_storage import FileStorage
from django.conf import settings
import tempfile
import hashlib
import os
import shutil
import models
from pathlib import Path

import api.models

from os.path import expanduser
home = expanduser("~")

options = {'STORAGE_PATH': home+'/.kipartman/version_storage', 'SUB_LEVELS': 3, 'SUB_LEVEL_SIZE': 2}


class VersionedFileStorage(object):

    def __init__(self, option=options):
        if not option:
            option = settings.FILE_STORAGE_OPTIONS

        self.storage_path = option['STORAGE_PATH']
        self.sub_levels = option['SUB_LEVELS']
        self.sub_level_size = option['SUB_LEVEL_SIZE']

    def get_sublevels(self, id):
        levels = []
        for level in range(self.sub_levels):
            start = level*self.sub_level_size
            stop = (level+1)*self.sub_level_size
            levels.append(id[start:stop])
        return levels

    def add_file(self, version_file):
        # get content
        file = tempfile.NamedTemporaryFile(delete=False)
        file.write(version_file.content)
        file.flush()
        file.close()
        
        # get md5
        md5 = hashlib.md5(version_file.content).hexdigest()
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
        storage_path = os.path.join(storage_path, os.path.basename(version_file.source_path))
        # copy file
        shutil.copyfile(file.name, os.path.join(dir, os.path.basename(version_file.source_path)))
        #TODO: Delete file.name from temp storage

        if version_file.id:
            ffile = models.VersionedFile.objects.get(pk=version_file.id)
            ffile.source_path = version_file.source_path
            ffile.storage_path = storage_path.replace('\\','/')
            ffile.md5 = md5
            ffile.version = version_file.version+1
            ffile.state = models.VersionedFileState.created
            ffile.updated = version_file.updated
            ffile.save()   
        else:
            # add file to db
            ffile = models.VersionedFile(source_path=version_file.source_path, 
                                        storage_path=storage_path.replace('\\','/'),
                                        md5=md5,
                                        version=1,
                                        state=models.VersionedFileState.created,
                                        updated=version_file.updated)
            ffile.save()
        
        print "Add file", version_file.source_path, "as", storage_path
        return file
    
    def get_file(self, id):
        levels = self.get_sublevels(id)
        dir = self.storage_path
        for level in levels:
            dir = dir+"/"+level
        return dir+"/"+id

    def get_status(self, file):
        #api.models.VersionedFile.objects.filter()
        # check if file exists in database
        pass
        
    def move_file(self, source_path, dest_path):
        pass
    
    def delete_file(self, file_path):
        pass
    
