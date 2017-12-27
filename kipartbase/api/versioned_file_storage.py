from file_storage import FileStorage

import api.models

class VersionedFileStorage(FileStorage):

    def __init__(self):
        super(VersionedFileStorage, self).__init__()

    def get_status(self, file):
        #api.models.VersionedFile.objects.filter()
        # check if file exists in database
        pass
    
    def add_file(self, file, file_path):
        pass
    
    def move_file(self, source_path, dest_path):
        pass
    
    def delete_file(self, file_path):
        pass
    
