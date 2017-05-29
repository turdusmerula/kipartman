import uuid
import shutil
import os
import ntpath
import models

class FileStorage(object):
    
    def __init__(self, storage_path='.', sub_levels=3, sub_level_size=2):
        self.storage_path = storage_path
        self.sub_levels = sub_levels
        self.sub_level_size = sub_level_size
    
    def get_sublevels(self, id):
        levels = []
        for level in range(self.sub_levels):
            start = level*self.sub_level_size
            stop = (level+1)*self.sub_level_size
            levels.append(id[start:stop])
        return levels

    def add_file(self, file_path):
        id = str(uuid.uuid1())
        
        # get folders sublevels
        levels = self.get_sublevels(id)
        # create sublevels
        dir = self.storage_path
        for level in levels:
            dir = dir+"/"+level
            if not os.path.exists(dir):
                os.makedirs(dir)
        # copy file
        shutil.copyfile(file_path, dir+"/"+id)

        # add file to db
        filename = ntpath.basename(file_path)
        file = models.File(id=id, filename=filename)
        models.File.objects.create(file)
        
        return id
    
    def get_file(self, id):
        levels = self.get_sublevels(id)
        dir = self.storage_path
        for level in levels:
            dir = dir+"/"+level
        return dir+"/"+id