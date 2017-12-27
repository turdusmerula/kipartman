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

class KicadResource(FileSystemEventHandler):
    def __init__(self):
        pass

class KicadResourcePretty(KicadResource):
    def __init__(self):
        super(KicadResourcePretty, self).__init__()
        self.files = {}
        
        self.load()
        
    def path(self):
        return configuration.kicad_library_path
            
    def on_any_event(self, event):
        print("Something happend with %s" % event.src_path)
        
    # - on_moved(self, event)
    # - on_created(self, event)
    # - on_deleted(self, event)
    # - on_modified(self, event)
    
    def load(self):
        """
        fill cache files from disk
        """
        self.files = {}
        libraries = self.GetLibraries()
        for library in libraries:
            footprints = self.GetFootprints(library)
            for footprint in footprints:
                source_path = os.path.join(library, footprint)
                md5 = hashlib.md5(os.path.join(configuration.kicad_library_path, source_path)).hexdigest()

                file = rest.model.VersionedFile()
                file.source_path = source_path
                file.md5 = md5
                file.updated = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(configuration.kicad_library_path, source_path))).strftime("%Y-%m-%dT%H:%M:%SZ")
                self.files[source_path] = file
        
    def GetLibraries(self, root_path=None):
        """
        Recurse all folders and return .pretty folders path
        @param root_path: path from which to start recursing, None starts from root
        """
        basepath = os.path.normpath(os.path.abspath(self.path()))
        to_explore = [basepath]
        libraries = []
        
        while len(to_explore)>0:
            path = to_explore.pop()
            if os.path.exists(path):
                for folder in glob(os.path.join(path, "*/")):
                    if folder!='/':
                        if re.compile("^.*\.pretty$").match(os.path.normpath(os.path.abspath(folder))):
                            print("=>", folder)
                            libraries.append(os.path.relpath(os.path.normpath(os.path.abspath(folder)), basepath))
                        elif os.path.normpath(os.path.abspath(folder))!=os.path.normpath(os.path.abspath(path)):
                            to_explore.append(folder)
    
        return libraries
    
    def GetFootprints(self, library_path):
        """
        Return all footprints in a pretty lib
        """
        footprints = []

        path = os.path.join(self.path(), library_path)        
        if os.path.exists(path):
            for kicad_mod in glob(os.path.join(path, "*.kicad_mod")):
                print("==>", kicad_mod)
                footprints.append(os.path.basename(kicad_mod))
    
        return footprints
    
    def Synchronize(self):
        """
        Get synchronization status from server
        """
        
        # get server content
        remote_footprints = rest.api.synchronize_versioned_files(self.files)


class KicadResourceManager(object):
    def __init__(self, resource):
        """
        Init a manager on a kicad resource
        @param resource: Kicad resource to manage (ex. KicadResourcePretty)
        """
        self.resource = resource

        self.observer = Observer()
        self.observer.schedule(resource, resource.path(), recursive=True)
        self.observer.start()

        # load local files
        resource.load()

        # load version configuration state
        self.version = sync.version_manager.VersionManager(resource.path())        
        self.version.load()

        # match
        self.files = {}
        self.match_files_version()
        
    def match_files_version(self):
        """
        Match local files with current stored version state 
        """
        for file in self.resource.files:
            file_version = None
            file_disk = self.resource.files[file]
            if self.version.Exist(file):
                file_version = self.version(file)           
            if file_version:
                if file_disk.md5!=file_version.md5:
                    file_version.state = 'outgo_change'
            else:
                file_version = rest.model.VersionedFile()
                file_version.source_path = file_disk.source_path
                file_version.state = 'outgo_add'
            self.files[file] = file_version
    
    def _debug(self):
        for file_path in self.files:
            file = self.files[file_path]
            if file.id:
                print("-- %s: %d '%s'"%(file_path, file.id, file.state)) 
            else:
                print("-- %s: None '%s'"%(file_path, file.state)) 
