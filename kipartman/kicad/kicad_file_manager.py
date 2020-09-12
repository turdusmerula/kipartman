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
from helper.exception import print_callstack, print_stack

class KicadFileManagerException(Exception):
    def __init__(self, error):
        super(KicadFileManagerException, self).__init__(error)

class File(object):
    def __init__(self, path):
        self.path = path
    
    @property
    def Path(self):
        return self.path
    
(FileChangedEvent, EVT_FILE_CHANGED) = wx.lib.newevent.NewEvent()

class KicadFileManager(wx.EvtHandler):

    observer = None
    event_handler = None
    
    path = {}
    path_handlers = {}
    
    class _CustomHandler(FileSystemEventHandler):
        def on_any_event(self, event):
            if hasattr(event, 'dest_path'): 
                wx.CallAfter(self.on_change_prehook, event.dest_path)
            elif hasattr(event, 'src_path'):
                wx.CallAfter(self.on_change_prehook, event.src_path)

        def on_change_prehook(self, path):
            path_changed = path
            
            while path!='/':
                if path in KicadFileManager.path_handlers:
                    for handler in KicadFileManager.path_handlers[path]:
                        wx.PostEvent(handler, FileChangedEvent(path=path_changed))
                        
                path = os.path.dirname(path)

    def __init__(self, owner, path):
        super(KicadFileManager, self).__init__()
        
        self._owner = owner
        
        if KicadFileManager.event_handler is None:
            KicadFileManager.event_handler = KicadFileManager._CustomHandler()
            
        if KicadFileManager.observer is None:
            KicadFileManager.observer = Observer()
        
        if KicadFileManager.observer.is_alive()==False:
            KicadFileManager.observer.start()
        
        self._path = path
        self._add_path(path)
        
    def __del__(self):
        self._remove_path(self.path)
    
    @staticmethod
    def _watch_from_path():
        KicadFileManager.observer.unschedule_all()
        
        path_to_watch = []
        for ipath in KicadFileManager.path:
            top_level = True
            for jpath in KicadFileManager.path:
                if ipath!=jpath and jpath.startswith(ipath):
                    top_level = False
            if top_level==True:
                path_to_watch.append(ipath)

        for path in path_to_watch:
            KicadFileManager.observer.schedule(KicadFileManager.event_handler, path, recursive=True)
            
    def _add_path(self, path):
        # each path can have several instances
        if path not in KicadFileManager.path:
            KicadFileManager.path[path] = 0
            KicadFileManager.path_handlers[path] = []
        KicadFileManager.path[path] += 1
        KicadFileManager.path_handlers[path].append(self._owner)
        
        self._watch_from_path()
        log.info(f"Added observer for {path}")

    def _remove_path(self, path):
        if path in KicadFileManager.path:
            KicadFileManager.path[path] -= 1
            KicadFileManager.path_handlers[path].remove(self._owner)
            
            if KicadFileManager.path[path] == 0:
                del KicadFileManager.path[path]
                del KicadFileManager.path_handlers[path]

        self._watch_from_path()
    
        log.info(f"Removed observer for {path}")
    
    @staticmethod
    def DisableNotificationsForPath(path, action, *args, **kwargs):
        KicadFileManager.observer.unschedule_all()

        handlers = []
        for handler in KicadFileManager.observer.Handlers:
            print("---", handler)
        
        res = None
        ex = None
        try:
            res = action(*args, **kwargs)
        except Exception as e:
            print(e)
            print_stack()
            ex = e

        KicadFileManager._watch_from_path()

        if ex is not None:
            raise ex
        return res
