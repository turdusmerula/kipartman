import os
import json
import rest
import re

class VersionManagerException(Exception):
    def __init__(self, error):
        self.error = error

class VersionManager(object):
    def __init__(self, root_path):
        self.root_path = root_path
        self.config = os.path.join(root_path, '.kiversion')
        
        # files from hard drive
        self.local_files = {}

        self.LoadState()
    
    def LoadState(self):
        state_files = {}
        
        if os.path.exists(self.config)==False:
            self.SaveState()
    
        content = json.load(open(self.config))
        for data in content:
            file = self.deserialize_file(data)
            state_files[file.source_path] = file
    
        self.SynchronizeState(state_files)
        
    def deserialize_file(self, json):
        file = rest.model.VersionedFile()
        if json.has_key('id'):
            file.id = int(json['id'])
        if json.has_key('source_path'):
            file.source_path = json['source_path']
        if json.has_key('storage_path'):
            file.storage_path = json['storage_path']
        if json.has_key('md5'):
            file.md5 = json['md5']
        if json.has_key('metadata'):
            file.metadata = unicode(json['metadata'])
        if json.has_key('version'):
            file.version = int(json['version'])
        if json.has_key('updated'):
            # fix wrong date format on reading
            updated = re.sub(
                       r" ", 
                       "T", 
                       json['updated']
                   ) 
            file.updated = updated
        file.state = ''
        if json.has_key('state'):
            file.state = json['state']
        return file
    
    def serialize_file(self, file):
        res = {}
        if file.id:
            res['id'] = unicode(file.id)
        if file.source_path:
            res['source_path'] = unicode(file.source_path)
        if file.storage_path:
            res['storage_path'] = unicode(file.storage_path)
        if file.metadata:
            res['metadata'] = unicode(file.metadata)
        if file.md5:
            res['md5'] = unicode(file.md5)
        if file.version:
            res['version'] = unicode(file.version)
        if file.updated:
            # TODO: handle correctly timezone
            res['updated'] = unicode(file.updated)
        if file.state:
            res['state'] = file.state
        return res 
        
    def SaveState(self):
        content = []
        for file in self.local_files:
            content.append(self.serialize_file(self.local_files[file]))

        with open(self.config, 'wb') as outfile:
            json.dump(content, outfile, sort_keys=True, indent=2, separators=(',', ': '))
            outfile.close()
    
    def SynchronizeState(self, state_files):
        """
        Synchronize local files with state
        """
        
        # Match local_files with current stored version state
        for file in self.local_files:
            file_version = None
            file_disk = self.local_files[file]
    
            # check if file exist in state
            if state_files.has_key(file):
                file_version = state_files[file]
            else:          
                # file not referenced in version state
                file_version = rest.model.VersionedFile()
                file_version.id = None 
                file_version.source_path = file_disk.source_path
                file_version.md5 = file_disk.md5
                file_version.version = None
                file_version.updated = file_disk.updated
                if file_version.state=="":
                    file_version.state = 'outgo_add'

            # check if local file changed toward state
            if file_disk.md5!=file_version.md5 and file_version.state=="":
                file_version.state = 'outgo_change'

            # update local file state 
            self.local_files[file] = file_version
        
        # Match stored version state with local files to detect removed files
        for file in state_files:
            file_version = state_files[file]
            file_disk = None
            
            # check if file exist in state
            if self.local_files.has_key(file):
                file_disk = self.local_files[file]
            else:
                # file not referenced in version state
                if os.path.exists(os.path.join(self.root_path, file))==True:    
                    file_disk = rest.model.VersionedFile()
                    file_disk.id = file_version.id 
                    file_disk.source_path = file_version.source_path
                    file_disk.md5 = file_version.md5
                    file_disk.version = file_version.version
                    file_disk.updated = file_version.updated
                    file_disk.metadata = file_version.metadata
                    if file_disk.state=="":
                        file_disk.state = 'outgo_del'

                    # update local file state 
                    self.local_files[file] = file_disk
        
        self.SaveState()
        
    def ClearLocalFiles(self):
        self.local_files.clear()
        
    def AddLocalFile(self, file):
        self.local_files[file.source_path] = file
    
    def Synchronize(self):
        """
        Return synchronization state from server
        """
        self.LoadState()
        
        # convert map to array
        files = []
        for file in self.local_files:
            files.append(self.local_files[file])

        if len(files)==0:
            # add dummy element, bug in swagger if list is empty it is handled as None
            files.append(rest.model.VersionedFile())
    
        # get synchronization state from server
        sync_files = {} 
        for file in rest.api.synchronize_versioned_files(files):
            sync_files[file.source_path] = file
            
            if file.state!='income_add' and file.state!='income_change' and file.state!='income_del' and file.state!='conflict_add' and file.state!='conflict_change' and file.state!='conflict_del': 
                self.local_files[file.source_path] = file
        
        self.SaveState()
        
        # match files between self.local_files and self.remote_files
        return sync_files

    def MoveFootprint(self, source, dest):
        if self.local_files.has_key(source)==False:
            raise VersionManagerException('Footprint %s does not exists'%source)
        file = self.local_files.pop(source)
        os.rename(os.path.join(self.root_path, source), os.path.join(self.root_path, dest))
        file.source_path = dest
        if file.version is None:
            file.state = 'outgo_add'
        else:
            file.state = 'outgo_change'
        self.local_files[dest] = file

        self.SaveState()
        
        return file
    
    def Commit(self, files):
        commits = rest.api.commit_versioned_files(files)
        
        # update state
        # TODO
        #for file in commits:
        #    self.state_files[file.source_path] = file
            
        self.SaveState()
        return commits
    
    def Update(self, files):
        updates = rest.api.update_versioned_files(files)
        
        # update state
        for file in updates:
            if file.state=='income_add' or file.state=='income_change':
                file.state = ''
                path = os.path.join(self.root_path, file.source_path)
                if os.path.exists(os.path.dirname(path))==False:
                    os.makedirs(os.path.dirname(path))
                with open(path, 'w') as write_file:
                    write_file.write(file.content)
                
                # check if file should be renamed
                local_file = None
                for local_file_name in self.local_files:
                    local_file = self.local_files[local_file_name]
                    if local_file.id==file.id:
                        break
                if local_file and local_file.source_path!=file.source_path:
                    self.Move(local_file.source_path, file.source_path)
                
                print "%%%", file
                self.local_files[file.source_path] = file
                
            elif file.state=='income_del':
                os.remove(os.path.join(self.root_path, file.source_path))
                self.local_files.pop(file.source_path)

        print "****", self.local_files
        
        self.SaveState()
        return updates        
    
    def AddFolder(self, path):
        abspath = os.path.join(self.root_path, path)
        if not os.path.exists(abspath):
            os.makedirs(abspath)
    
    def RenameFolder(self, path, newname):
        pass
    
    def RenameLibrary(self, path, newname):
        pass
    
    
    def DeleteFolder(self, path):
        pass
    
    def DeleteLibrary(self, path):
        pass
    
    def UpdateMetadata(self, path, metadata):
        if self.local_files.has_key(path):
            print "*****", path, metadata
            self.local_files[path].metadata = metadata
            self.SaveState()
                  
    def _debug(self, files):
        for file_path in files:
            file = files[file_path]
            if file.id:
                print("-- %s: %d '%s'"%(file_path, file.id, file.state)) 
            else:
                print("-- %s: None '%s'"%(file_path, file.state)) 
