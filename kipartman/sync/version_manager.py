import os
import json
import rest

class VersionManager(object):
    def __init__(self, root_path):
        self.root_path = root_path
        self.config = os.path.join(root_path, '.kiversion')
        self.local_files = {}
        self.remote_files = {}
        
    def load(self):
        if os.path.exists(self.config)==False:
            self.save()
    
        content = json.load(open(self.config))
        for data in content:
            file = rest.model.VersionedFile(**data)
            self.file.append(file)

    def save(self):
        content = []
        for file in self.local_files:
            content.append(self.local_files[file])

        with open(self.config, 'wb') as outfile:
            json.dump(content, outfile, sort_keys=True, indent=2, separators=(',', ': '))

    def Synchronize(self, files):
        # match files between self.local_files and self.remote_files
        # 
        pass
    
    def Exist(self, path):
        return self.local_files.has_key(path)

    def Files(self):
        return self.local_files
    
    def File(self, path):
        if self.local_files.has_key(path):
            return self.files[path]
        return None
