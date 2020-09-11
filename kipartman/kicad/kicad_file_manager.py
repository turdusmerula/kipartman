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
    # map with path / observer
    observer = None
    
#     observers = {}
#     notifiers = []

    class _CustomHandler(FileSystemEventHandler):
        def on_any_event(self, event):
#             if self.enabled==False:
#                 return 
#     
#             self.enabled = False
#             for extension in self.extensions:
#                 if hasattr(event, 'dest_path') and os.path.isfile(event.dest_path) and os.path.basename(event.dest_path).startswith('.')==False and event.dest_path.endswith('.'+extension):
#                     print("-", self)
#                     log.info("Something happend with %s" % (event.dest_path))
#                     path = os.path.relpath(event.dest_path, self.watch_path)
#                     self.on_change_prehook(path)
#                     if self.on_change_hook:
#                         wx.CallAfter(self.on_change_hook, path)
#                 elif hasattr(event, 'src_path') and os.path.isfile(event.src_path) and os.path.basename(event.src_path).startswith('.')==False and event.src_path.endswith('.'+extension):
#                     print("+", self)
#                     log.info("Something happend with %s" % (event.src_path))
#                     path = os.path.relpath(event.src_path, self.watch_path)
#                     self.on_change_prehook(path)
#                     if self.on_change_hook:
#                         wx.CallAfter(self.on_change_hook, path)
#             self.enabled = True
            print("+++", self, event)
            
    def __init__(self, watch_path, extensions):
        if KicadFileManager.observer is None:
            KicadFileManager.observer = Observer()
        
        if KicadFileManager.observer.is_alive()==False:
            KicadFileManager.observer.start()

        self.event_handler = KicadFileManager._CustomHandler()
        self.watch_path = watch_path
        KicadFileManager.observer.schedule(self.event_handler, watch_path, recursive=True)
        
        return
#     FileSystemEventHandler
#         self.on_change_hook = None
#         
#         self.watch_path = watch_path
#         self.extensions = extensions
#         
#         if os.path.exists(self.watch_path)==False:
#             os.makedirs(self.watch_path)
# 
#         # observer to trigger event on resource change
#         self.enabled = True
# 
#         if self.watch_path in KicadFileManager.observers:
#             self.observer = KicadFileManager.observers[self.watch_path]
#         else:
#             self.observer = Observer()
#             KicadFileManager.observers[self.watch_path] = self.observer
#             self.observer.start()
#         
#         KicadFileManager.notifiers.append(self)
#         
#         self.watch = self.observer.schedule(self, self.watch_path, recursive=True)
#         
#         log.info(f"Added file observer at {self.watch_path}")

    def __del__(self):
        return
#         self.observer.remove_handler_for_watch(self, self.watch)
#         KicadFileManager.notifiers.remove(self)


#         def on_created(self, event):
#             _check_modification(event.src_path)
# 
#         def on_modified(self, event):
#             _check_modification(event.src_path)
# 
#         def on_moved(self, event):
#             _check_modification(event.src_path)
#             _check_modification(event.dest_path)
# 
#         def on_deleted(self, event):
#             _check_modification(event.src_path)
    
    def on_change_prehook(self, path):
        pass
    
#     def Enabled(self, enabled=True):
#         if enabled:
#             if self.watch is None:
#                 self.watch = self.observer.schedule(self, self.watch_path, recursive=True)
#         else:
#             if self.watch is not None:
#                 self.observer.unschedule(self.watch)
#             self.watch = None

    @staticmethod
    def DisableNotificationsForPath(path, action, *args, **kwargs):
#         print("-", path)
# #         for observer_path in KicadFileManager.observers:
# #             if os.path.normpath(path).startswith(os.path.normpath(notifier.watch_path)):
#         for notifier in KicadFileManager.notifiers:
#             if os.path.normpath(path).startswith(os.path.normpath(notifier.watch_path)):
#                 print("--", notifier.watch_path)
#                 notifier.Enabled(False)
#         
        res = None
        ex = None
        try:
            res = action(*args, **kwargs)
        except Exception as e:
            print(e)
            print_stack()
            ex = e
#             
#         for notifier in KicadFileManager.notifiers:
#             if os.path.normpath(path).startswith(os.path.normpath(notifier.watch_path)):
#                 print("++", notifier.watch_path)
#                 notifier.Enabled(True)
#         
        if ex is not None:
            raise ex
        return res
    
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
        os.makedirs(path)
    
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
