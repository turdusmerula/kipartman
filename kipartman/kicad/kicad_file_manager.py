from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from configuration import configuration
from glob import glob
import os
import re
import helper.hash as hash
from pathlib2 import Path
import shutil
import json
import wx
from helper.log import log
from helper.exception import print_callstack

class KicadFileManagerException(Exception):
    def __init__(self, error):
        super(KicadFileManagerException, self).__init__(error)

class File(object):
    def __init__(self, path):
        self.path = path
    
    @property
    def Path(self):
        return self.path
    
class KicadFileManager(FileSystemEventHandler):
    # map with path / observer
    observers = {}
    
    def __init__(self, root_path):
        self.on_change_hook = None
        
        self.root_path = root_path
        self.files = {}
        self.folders = []
        self.extensions = []
        
        if os.path.exists(self.root_path)==False:
            os.makedirs(self.root_path)

        # observer to trigger event on resource change
        self.enabled = True

        if self.root_path in KicadFileManager.observers:
            self.observer = KicadFileManager.observers[self.root_path]
        else:
            self.observer = Observer()
            KicadFileManager.observers[self.root_path] = self.observer
            self.observer.start()
        
        self.watch = self.observer.schedule(self, self.root_path, recursive=True)
        
        log.info(f"Added file observer at {self.root_path}")

    def __del__(self):
        self.observer.remove_handler_for_watch(self, self.watch)

    
    def version_file(self):
        return '.kiversion'
    
    def category(self):
        return ''

    def on_any_event(self, event):
        if self.enabled==False:
            return 
        
        print_callstack() 
        
        self.enabled = False
        for extension in self.extensions:
            if hasattr(event, 'dest_path') and os.path.isfile(event.dest_path) and os.path.basename(event.dest_path).startswith('.')==False and event.dest_path.endswith('.'+extension):
                log.info("Something happend with %s" % (event.dest_path))
                path = os.path.relpath(event.dest_path, self.root_path())
                self.on_change_prehook(path)
                if self.on_change_hook:
                    wx.CallAfter(self.on_change_hook, path)
            elif hasattr(event, 'src_path') and os.path.isfile(event.src_path) and os.path.basename(event.src_path).startswith('.')==False and event.src_path.endswith('.'+extension):
                log.info("Something happend with %s" % (event.src_path))
                path = os.path.relpath(event.src_path, self.root_path())
                self.on_change_prehook(path)
                if self.on_change_hook:
                    wx.CallAfter(self.on_change_hook, path)
        
        self.enabled = True
    # - on_moved(self, event)
    # - on_created(self, event)
    # - on_deleted(self, event)
    # - on_modified(self, event)
    
    def on_change_prehook(self, path):
        pass
    
    def Enabled(self, enabled=True):
        if enabled:
            if self.watch is None:
                self.watch = self.observer.schedule(self, self.root_path(), recursive=True)
        else:
            if self.watch:
                self.observer.unschedule(self.watch)
            self.watch = None

    def Load(self):
        pass

    def Exists(self, path):
        return False

    def CreateFile(self, path, content, overwrite=False):        
        return None
    
    def EditFile(self, file, content, create=False):           
        return None, False
    
    def MoveFile(self, file, dest_path, force=False):
        return None

    def DeleteFile(self, file, force=False):
        return None
    
    def CreateFolder(self, path):
        pass
    
    def MoveFolder(self, source_path, dest_path):
        pass
    
    def DeleteFolder(self, path):
        pass

    def LoadContent(self, file):
        pass

    def LoadMetadata(self, file):
        return {}

    def EditMetadata(self, path, metadata):
        return metadata
