from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from configuration import configuration
from glob import glob
import os
import re

class KicadResource(FileSystemEventHandler):
    def __init__(self):
        pass

class KicadResourcePretty(KicadResource):
    def __init__(self):
        super(KicadResourcePretty, self).__init__()

    def path(self):
        return configuration.kicad_library_path
            
    def on_any_event(self, event):
        print("Something happend with %s" % event.src_path)
       
    # - on_moved(self, event)
    # - on_created(self, event)
    # - on_deleted(self, event)
    # - on_modified(self, event)

    def GetLibraries(self):
        """
        Recurse all folders and return .pretty folders path
        """
        basepath = os.path.normpath(os.path.abspath(self.path()))
        to_explore = [basepath]
        libraries = []
        
        while len(to_explore)>0:
            path = to_explore.pop()
            if os.path.exists(path):
                print("---", path)
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
                print("=>", kicad_mod)
                footprints.append(os.path.basename(kicad_mod))
    
        return footprints
    
class KicadResourceManager(object):
    def __init__(self, resource):
        self.resource = resource

        self.observer = Observer()
        self.observer.schedule(resource, resource.path(), recursive=True)
        self.observer.start()
