from file_storage import FileStorage
from django.conf import settings
import tempfile
import hashlib
import os
import shutil
import models
from pathlib import Path
import datetime

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

    def get_storage_path(self, version_file):
        md5 = hashlib.md5(version_file.content).hexdigest()
        levels = self.get_sublevels(md5)
        
        # get current sublevel
        storage_path = self.storage_path

        # create sublevels
        for level in levels:
            storage_path = os.path.join(storage_path, level)
        storage_path = os.path.join(storage_path, md5, os.path.basename(version_file.source_path))

        return storage_path
    
    def add_file(self, version_file):
        storage_path = self.get_storage_path(version_file)

        if not os.path.exists(os.path.dirname(storage_path)):
            os.makedirs(os.path.dirname(storage_path))
        
        # create file
        md5 = hashlib.md5(version_file.content).hexdigest()
        with open(os.path.join(self.storage_path, storage_path), 'wb') as outfile:
            outfile.write(version_file.content)
            outfile.close()

        if version_file.id:
            ffile = models.VersionedFile.objects.get(pk=version_file.id)
            ffile.source_path = version_file.source_path
            ffile.storage_path = storage_path.replace('\\','/')
            ffile.md5 = md5
            ffile.version = ffile.version+1                
            ffile.state = models.VersionedFileState.created
            ffile.updated = datetime.datetime.now()
            ffile.metadata = version_file.metadata
            ffile.category = version_file.category
            ffile.save()   
        else:
            # add file to db
            ffile = models.VersionedFile(source_path=version_file.source_path, 
                                        storage_path=storage_path.replace('\\','/'),
                                        md5=md5,
                                        version=1,
                                        state=models.VersionedFileState.created,
                                        updated=datetime.datetime.now(),
                                        metadata=version_file.metadata,
                                        category=version_file.category)
            ffile.save()
        
        version_file.id = ffile.id
        version_file.storage_path = ffile.storage_path
        version_file.md5 = md5
        version_file.version = ffile.version
        version_file.updated = ffile.updated 
        version_file.category = ffile.category 
        version_file.state = ''
        
        print "Add file", version_file.source_path, "as", storage_path
        return version_file
    
    def delete_file(self, version_file):
        #storage_path = os.path.join(self.storage_path, version_file.storage_path)

        ffile = models.VersionedFile.objects.get(pk=version_file.id)
        ffile.state = models.VersionedFileState.deleted
        ffile.updated = datetime.datetime.now()
        ffile.version = ffile.version+1                
        ffile.save()   
        
        version_file.storage_path = None
        version_file.state = ''
        
        print "Delete file", version_file.source_path
        return version_file
        
    def get_file_content(self, id):
        ffile = models.VersionedFile.objects.get(pk=id)
        file = os.path.join(self.storage_path, ffile.storage_path)
        with open(file, 'r') as content_file:
            return content_file.read()
        return ''
        