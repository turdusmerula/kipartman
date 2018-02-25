from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from configuration import configuration
from glob import glob
import os
import re
import rest
import datetime, time
import hashlib
import sync.version_manager
from pathlib2 import Path
from helper.exception import print_stack
import shutil

import rest

class KicadFileManagerException(Exception):
    def __init__(self, error):
        super(KicadFileManagerException, self).__init__(error)

class KicadFileManager(FileSystemEventHandler):
    def __init__(self):
        pass

class KicadFileManagerPretty(KicadFileManager):
    def __init__(self):
        super(KicadFileManagerPretty, self).__init__()
        self.on_change_hooks = []
        self.enabled = True

        self.files = {}
        self.folders = []
        
        # observer to trigger event on resource change
        self.observer = Observer()
        self.observer.schedule(self, self.root_path(), recursive=True)
        self.observer.start()

      
    def root_path(self):
        return configuration.kicad_library_path
            
    def on_any_event(self, event):
        if self.enabled==False:
            return 
        
        if os.path.basename(event.src_path)!='.kiversion':
            print("Something happend with %s" % event.src_path)
            for hook in self.on_change_hooks:
                hook(event)
    # - on_moved(self, event)
    # - on_created(self, event)
    # - on_deleted(self, event)
    # - on_modified(self, event)
    
    def Enabled(self, enabled=True):
        self.enabled = enabled

    def AddChangeHook(self, hook):
        self.on_change_hooks.append(hook)

    def Load(self):
        """
        fill cache files from disk
        """
        self.files = {}
        libraries, self.folders = self.GetLibraries()
        
        for library in libraries:
            footprints = self.GetFootprints(library)
            for footprint in footprints:
                source_path = os.path.join(library, footprint)
                content = Path(os.path.join(configuration.kicad_library_path, source_path)).read_text()
                md5 = hashlib.md5(content).hexdigest()
 
                file = rest.model.VersionedFile()
                file.source_path = source_path
                file.md5 = md5

                self.files[source_path] = file


    def GetLibraries(self, root_path=None):
        """
        Recurse all folders and return .pretty folders path
        @param root_path: path from which to start recursing, None starts from root
        """
        print "===> GetLibraries----"
        basepath = os.path.normpath(os.path.abspath(self.root_path()))
        to_explore = [basepath]
        libraries = []
        folders = []
        
        while len(to_explore)>0:
            path = to_explore.pop()
            if os.path.exists(path):
                for folder in glob(os.path.join(path, "*/")):
                    if folder!='/':
                        folders.append(os.path.relpath(os.path.normpath(os.path.abspath(folder)), basepath))
                        if re.compile("^.*\.pretty$").match(os.path.normpath(os.path.abspath(folder))):
                            print "=>", folder 
                            libraries.append(os.path.relpath(os.path.normpath(os.path.abspath(folder)), basepath))
                        elif os.path.normpath(os.path.abspath(folder))!=os.path.normpath(os.path.abspath(path)):
                            to_explore.append(folder)
        print "---------------------"
     
        return libraries, folders

    def GetFootprints(self, library_path):
        """
        Return all footprints in a pretty lib
        """
        print "===> GetFootprints----"
        footprints = []
 
        path = os.path.join(self.root_path(), library_path)        
        if os.path.exists(path):
            for kicad_mod in glob(os.path.join(path, "*.kicad_mod")):
                print "==>", kicad_mod 
                footprints.append(os.path.basename(kicad_mod))
        print "----------------------"
     
        return footprints
 
    def Exists(self, path):
        return os.path.exists(os.path.join(self.root_path(), path))

    def CreateFile(self, path, content, overwrite=False):
        if self.Exists(path) and overwrite==False:
            raise KicadFileManagerException('File %s already exists'%path)

        fullpath = os.path.join(self.root_path(), path)
        if not os.path.exists(os.path.dirname(fullpath)):
            os.makedirs(os.path.dirname(fullpath))
        
        with open(fullpath, 'w') as content_file:
            if content:
                content_file.write(content)
            else:
                content_file.write('')
        content_file.close() 

        file = rest.model.VersionedFile()
        file.source_path = path
        file.md5 = hashlib.md5(content).hexdigest()
        file.updated = rest.api.get_date()
        
        return file
    
    def EditFile(self, file, content, create=False):
        if self.Exists(file.source_path)==False and create==False:
            raise KicadFileManagerException('File %s does not exists'%file.source_path)

        fullpath = os.path.join(self.root_path(), file.source_path)
        if self.Exists(file.source_path)==True:
            md5file = hashlib.md5(Path(fullpath).read_text()).hexdigest()
            md5 = hashlib.md5(content).hexdigest()
            if md5==md5file:
                return file, False
        
        if os.path.exists(os.path.dirname(fullpath))==False:
            os.makedirs(os.path.dirname(fullpath))
        with open(fullpath, 'w') as content_file:
            if content:
                content_file.write(content)
            else:
                content_file.write('')
        content_file.close() 
 
        file.md5 = hashlib.md5(content).hexdigest()
        file.updated = rest.api.get_date()
           
        return file, True
    
    def MoveFile(self, file, dest_path, force=False):
        if self.Exists(file.source_path)==False and force==False:
            raise KicadFileManagerException('File %s does not exists'%file.source_path)
        if self.Exists(dest_path) and force==False:
            raise KicadFileManagerException('File %s already exists'%dest_path)
        
        os.rename(os.path.join(self.root_path(), file.source_path), 
                         os.path.join(self.root_path(), dest_path))

        file.source_path = dest_path
        #fullpath = os.path.join(self.root_path(), file.source_path)
        #file.updated = datetime.datetime.fromtimestamp(os.path.getmtime(fullpath)).strftime("%Y-%m-%dT%H:%M:%SZ")
        file.updated = rest.api.get_date()
        
        return file

    def DeleteFile(self, file, force=False):
        if self.Exists(file.source_path)==False and force==False:
            raise KicadFileManagerException('File %s does not exists'%file.source_path)
        
        fullpath = os.path.join(self.root_path(), file.source_path)
        if os.path.exists(fullpath):
            os.remove(fullpath)
        #file.updated = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        file.updated = rest.api.get_date()
    
        return file
    
    def LoadContent(self, file):
        if self.Exists(file.source_path)==False:
            raise KicadFileManagerException('File %s does not exists'%file.source_path)
        
        fullpath = os.path.join(self.root_path(), file.source_path)
        with open(fullpath) as f:
            file.content = f.read()

            
    def CreateFolder(self, path):
        abspath = os.path.join(self.root_path(), path)
        if os.path.exists(abspath):
            raise KicadFileManagerException('Folder %s already exists'%path)
        else:
            os.makedirs(abspath)
    
    def MoveFolder(self, source_path, dest_path):
        abs_source_path = os.path.join(self.root_path(), source_path)
        abs_dest_path = os.path.join(self.root_path(), dest_path)
        if os.path.exists(abs_source_path)==False:
            raise KicadFileManagerException('Folder %s does not exists'%abs_source_path)
        if os.path.exists(abs_dest_path):
            raise KicadFileManagerException('Folder %s already exists'%abs_dest_path)
        shutil.move(abs_source_path, abs_dest_path)
    
    def DeleteFolder(self, path):
        abspath = os.path.join(self.root_path(), path)
        shutil.rmtree(abspath)
      