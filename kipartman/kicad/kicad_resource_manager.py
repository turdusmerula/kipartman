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
#import quopri

class KicadResource(FileSystemEventHandler):
    def __init__(self):
        pass

class KicadResourcePretty(KicadResource):
    def __init__(self):
        super(KicadResourcePretty, self).__init__()
        self.files = {}
        self.folders = []
        self.on_change = None
        self.enabled = True
        
        self.Load()
        
    def path(self):
        return configuration.kicad_library_path
            
    def on_any_event(self, event):
        print("Something happend with %s" % event.src_path)
        if os.path.basename(event.src_path)!='.kiversion' and self.on_change and self.enabled:
            self.on_change(event)
    # - on_moved(self, event)
    # - on_created(self, event)
    # - on_deleted(self, event)
    # - on_modified(self, event)
    
    def Enabled(self, enabled=True):
        self.enabled = enabled
        
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
        folders = []
        
        while len(to_explore)>0:
            path = to_explore.pop()
            if os.path.exists(path):
                for folder in glob(os.path.join(path, "*/")):
                    if folder!='/':
                        folders.append(os.path.relpath(os.path.normpath(os.path.abspath(folder)), basepath))
                        if re.compile("^.*\.pretty$").match(os.path.normpath(os.path.abspath(folder))):
                            print("=>", folder)
                            libraries.append(os.path.relpath(os.path.normpath(os.path.abspath(folder)), basepath))
                        elif os.path.normpath(os.path.abspath(folder))!=os.path.normpath(os.path.abspath(path)):
                            to_explore.append(folder)
    
        return libraries, folders

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

    def Files(self):
        return self.files

class KicadResourceManager(sync.version_manager.VersionManager):
    def __init__(self, resource):
        """
        Init a manager on a kicad resource
        @param resource: Kicad resource to manage (ex. KicadResourcePretty)
        """
        super(KicadResourceManager, self).__init__(resource.path())        

        # resource to observe
        self.resource = resource

        # observer to trigger event on resource change
        self.observer = Observer()
        self.observer.schedule(resource, resource.path(), recursive=True)
        self.observer.start()

        self.load()

    def load(self):
        # load local files
        self.resource.Load()

        # load version configuration state
        self.LoadState()

    def Synchronize(self):
        self.load()
        
        # refresh local files state before synchronizing
        self.ClearLocalFiles()
        files = self.resource.Files()
        for file in files:
            self.AddLocalFile(files[file])
        
        return super(KicadResourceManager, self).Synchronize()

    def Commit(self, files):
        # add content
        for file in files:
            if file.state!='income_add' and file.state!='income_change' and file.state!='income_del':
                with open(os.path.join(self.resource.path(), file.source_path)) as f:
                    file.content = f.read()
        
        return super(KicadResourceManager, self).Commit(files)
    
