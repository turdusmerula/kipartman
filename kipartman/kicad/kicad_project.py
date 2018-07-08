from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from configuration import configuration
from glob import glob
import os
import re
import hashlib
from pathlib2 import Path
import shutil
import json
import rest
import wx

class KicadProjectException(Exception):
    def __init__(self, error):
        super(KicadProjectException, self).__init__(error)

class KicadProject(FileSystemEventHandler):
    def __init__(self, project_file):
        self.on_change_hook = None
        
        self.files = {}
        self.folders = []
        self.extensions = ['bom', 'net', 'sch', 'kicad_pcb']
        
        self.project_file = project_file
        self.root_path = os.path.dirname(self.project_file)
        
        # observer to trigger event on resource change
        self.enabled = True
        self.observer = Observer()
        self.watch = self.observer.schedule(self, self.root_path, recursive=True)
        self.observer.start()
    
    def on_any_event(self, event):
        if self.enabled==False:
            return 
        
        self.enabled = False
        for extension in self.extensions:
            if hasattr(event, 'dest_path') and os.path.isfile(event.dest_path) and os.path.basename(event.dest_path).startswith('.')==False and event.dest_path.endswith('.'+extension):
                print("Something happend with %s" % (event.dest_path))
                path = os.path.relpath(event.dest_path, self.root_path)
                if self.on_change_hook:
                    wx.CallAfter(self.on_change_hook, path)
            elif hasattr(event, 'src_path') and os.path.isfile(event.src_path) and os.path.basename(event.src_path).startswith('.')==False and event.src_path.endswith('.'+extension):
                print("Something happend with %s" % (event.src_path))
                path = os.path.relpath(event.src_path, self.root_path)
                if self.on_change_hook:
                    wx.CallAfter(self.on_change_hook, path)
        
        self.enabled = True
    # - on_moved(self, event)
    # - on_created(self, event)
    # - on_deleted(self, event)
    # - on_modified(self, event)
        
    def Enabled(self, enabled=True):
        if enabled:
            if self.watch is None:
                self.watch = self.observer.schedule(self, self.root_path, recursive=True)
        else:
            if self.watch:
                self.observer.unschedule(self.watch)
            self.watch = None

    def Load(self):
        """
        fill cache files from disk
        """
        self.files, self.folders = self.GetFiles()
        
    def GetFiles(self):
        """
        Recurse all folders and return kicad files and folders path
        """
        basepath = os.path.normpath(os.path.abspath(self.root_path))
        to_explore = [basepath]
        files = []
        folders = []
        
        while len(to_explore)>0:
            path = to_explore.pop()
            if os.path.exists(path):
                for file in glob(os.path.join(path, "*")):
                    if os.path.isfile(file):
                        for ext in self.extensions:
                            if os.path.normpath(os.path.abspath(file)).endswith(ext):
                                files.append(os.path.relpath(os.path.normpath(os.path.abspath(file)), basepath))
                    else:
                        folder = file
                        if folder!='/':
                            folders.append(os.path.relpath(os.path.normpath(os.path.abspath(folder)), basepath))
                            if os.path.normpath(os.path.abspath(folder))!=os.path.normpath(os.path.abspath(path)):
                                to_explore.append(folder)
     
        return files, folders
