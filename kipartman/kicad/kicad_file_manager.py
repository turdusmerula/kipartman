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

class KicadFileManagerException(Exception):
    def __init__(self, error):
        super(KicadFileManagerException, self).__init__(error)

class KicadFileManager(FileSystemEventHandler):
    def __init__(self):
        self.on_change_hook = None
        
        self.files = {}
        self.folders = []
        self.extensions = []
        
        if os.path.exists(self.root_path())==False:
            os.makedirs(self.root_path())

        # observer to trigger event on resource change
        self.enabled = True
        self.observer = Observer()
        self.watch = self.observer.schedule(self, self.root_path(), recursive=True)
        self.observer.start()
    
    def version_file(self):
        return '.kiversion'
    
    def category(self):
        return ''

    def on_any_event(self, event):
        if self.enabled==False:
            return 
        
        self.enabled = False
        for extension in self.extensions:
            if hasattr(event, 'dest_path') and os.path.isfile(event.dest_path) and os.path.basename(event.dest_path).startswith('.')==False and event.dest_path.endswith('.'+extension):
                print("Something happend with %s" % (event.dest_path))
                path = os.path.relpath(event.dest_path, self.root_path())
                self.on_change_prehook(path)
                if self.on_change_hook:
                    wx.CallAfter(self.on_change_hook, path)
            elif hasattr(event, 'src_path') and os.path.isfile(event.src_path) and os.path.basename(event.src_path).startswith('.')==False and event.src_path.endswith('.'+extension):
                print("Something happend with %s" % (event.src_path))
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

class KicadFileManagerPretty(KicadFileManager):
    def __init__(self):
        super(KicadFileManagerPretty, self).__init__()

        self.extensions = ['kicad_mod']
        
    def root_path(self):
        return configuration.kicad_footprints_path

    def version_file(self):
        return '.kiversion_mod'

    def category(self):
        return 'pretty'
    
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
                content = Path(os.path.join(self.root_path(), source_path)).read_text()
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
        file.category = self.category()

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
     

def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail

class KicadLibCacheElement(object):
    def __init__(self, content='', metadata={}):
        self.content = content
        self.metadata = metadata

    def text_metadata(self):
        res = ''
        for metadata in self.metadata:
            if metadata=='K' or metadata=='D':
                if res!='':
                    res = res+'\n'
                res = res+metadata+' '+self.metadata[metadata]
        return res

   
class KicadLibCache(object):
    def __init__(self, root_path):
        self.libs = {}
        self.root_path = root_path
        
    def read_lib_file(self, lib):
        symbols = {}

        lib_path = os.path.join(self.root_path, lib)
        
        if(os.path.isfile(lib_path)==False):
            return []

        content = ''
        name = ''
        for line in open(lib_path, 'r'):

            if line.startswith("EESchema-LIBRARY"):
                pass
            elif line.startswith("#encoding"):
                pass
            elif line.startswith("#"):
                pass
                #content = content+line
            elif line.startswith("DEF"):
                content = content+line
                name = line.split(' ')[1]+'.mod'
            elif line.startswith("ENDDEF"):
                content = content+line
                symbols[name] = content
                content = ''
            else:
                content = content+line
                
        return symbols

    def read_metadata_file(self, lib):
        metadata = {}
        
        dcm = re.sub(r"\.lib$", ".dcm", lib)
        dcm_path = os.path.join(self.root_path, dcm)
        
        if(os.path.isfile(dcm_path)==False):
            return None

        name = ''
        for line in open(dcm_path, 'r'):
            line = line.replace('\n', '')
            if line.startswith("EESchema-DOCLIB"):
                pass
            elif line.startswith("#"):
                pass
            elif line.startswith("$CMP"):
                name = line.split(' ')[1]+'.mod'
                metadata[name] = {}
            elif line.startswith("$ENDCMP"):
                name = ''
            elif name!='':
                label = line.split(' ')[0]
                value = " ".join(line.split(' ')[1:])
                metadata[name][label] = value
        
        return metadata
        
    def Clear(self, path=None):
        if path:
            if path.endswith('.lib'):
                if self.libs.has_key(path):
                    self.libs.pop(path)
            elif path.endswith('.mod'):
                library = re.sub(r"\.lib.*\.mod$", ".lib", path)
                symbol = re.sub(r"^.*\.lib.", "", path)
                if self.libs.has_key(library) and self.libs[library].has_key(symbol):
                    self.libs[library].pop(symbol)
        else:
            self.libs = {}
        
    def GetSymbol(self, symbol_path):
        library = re.sub(r"\.lib.*\.mod$", ".lib", symbol_path)
        symbol = re.sub(r"^.*\.lib.", "", symbol_path)

        if self.libs.has_key(library) and self.libs[library].has_key(symbol):
            return self.libs[library][symbol]
        else:
            symbols = self.read_lib_file(library)
            metadata = self.read_metadata_file(library)
            self.libs[library] = {}
            for symbol in symbols:
                if metadata.has_key(symbol):
                    meta = metadata[symbol]
                print "%$$$", meta
                self.libs[library][symbol] = KicadLibCacheElement(content=symbols[symbol], metadata=meta)

        if self.libs.has_key(library) and self.libs[library].has_key(symbol):
            return self.libs[library][symbol]
        return None
        
    def GetSymbols(self, lib_path):
        if self.libs.has_key(lib_path):
            return self.libs[lib_path]
        else:
            symbols = self.read_lib_file(lib_path)
            metadata = self.read_metadata_file(lib_path)
            self.libs[lib_path] = {}
            for symbol in symbols:
                meta = {}
                if metadata.has_key(symbol):
                    meta = metadata[symbol]
                print "%$$$", symbol, meta
                self.libs[lib_path][symbol] = KicadLibCacheElement(content=symbols[symbol], metadata=meta)
        
        if self.libs.has_key(lib_path):
            return self.libs[lib_path]
        return {}
    
    def update_content(self, name, content):
        new_content = ''
        has_def = False
        for line in content.split('\n'):
            if line.startswith('#'):
                pass
            elif line.startswith('DEF'):
                els = line.split(' ')
                els[1] = name
                if new_content!='':
                    new_content = new_content+'\n'
                new_content = new_content+" ".join(els)
                has_def = True
            else:
                if new_content!='':
                    new_content = new_content+'\n'
                new_content = new_content+line
#        content = "#\n"+content    
#        content = "# "+name+'\n'+content    
#        content = "#\n"+content    

        if has_def==False:
            new_content = new_content+"DEF "+name+" RF 0 40 Y N 1 F N\n"
            new_content = new_content+"DRAW\n"
            new_content = new_content+"ENDDRAW\n"
            new_content = new_content+"ENDDEF\n"
            
        return new_content
    
    def AddSymbol(self, path, content, metadata):
        library = re.sub(r"\.lib.*\.mod$", ".lib", path)
        symbol = re.sub(r"^.*\.lib.", "", path)
        symbol_name = re.sub(r".mod$", "", os.path.basename(path))
        
        content = self.update_content(symbol_name, content)
        if self.libs.has_key(library)==False:
            self.libs[library] = {}
        self.libs[library][symbol] = KicadLibCacheElement(content, metadata)
        
    def Exists(self, path):
        if path.endswith('.mod'):
            library = re.sub(r"\.lib.*\.mod$", ".lib", path)
            symbol = re.sub(r"^.*\.lib.", "", path)
            
            symbols = self.GetSymbols(library)
            if symbols and symbols.has_key(symbol):
                return True
            return False
        elif path.endswith('.lib'):
            if self.GetSymbols(path):
                return True
            return False
        else:
            return os.path.exists(os.path.join(self.root_path, path))
        
class KicadFileManagerLib(KicadFileManager):
    """
    Simulate lib files as a folder containing symbol files
    """
    def __init__(self):
        super(KicadFileManagerLib, self).__init__()
        self.lib_cache = KicadLibCache(self.root_path())
        self.extensions = ['lib', 'dcm']
        
    def version_file(self):
        return '.kiversion_lib'

    def root_path(self):
        return configuration.kicad_symbols_path

    def category(self):
        return 'lib'

    def on_change_prehook(self, path):
# #         # discard cache
#         if path.endswith(".dcm"):
#             self.lib_cache.Clear(re.sub(r"\.dcm$", ".lib", path))
#         if path.endswith(".lib"):
#             self.lib_cache.Clear(path)
        pass
    
    def Load(self):
        """
        fill cache files from disk
        """
        self.files = {}
        libraries, self.folders = self.GetLibraries()
        self.lib_cache.Clear()
        
        for library in libraries:
            symbols = self.GetSymbols(library)
            for symbol in symbols:
                file = rest.model.VersionedFile()
                file.source_path = symbol
                self.LoadContent(file)
                file.md5 = hashlib.md5(file.content).hexdigest()
                file.category = self.category()
                file.metadata = self.LoadMetadata(symbol)
                
                self.files[file.source_path] = file
    
    def GetLibraries(self, root_path=None):
        """
        Recurse all folders and return .lib files path
        @param root_path: path from which to start recursing, None starts from root
        """
        print "===> GetLibraries----"
        basepath = os.path.normpath(os.path.abspath(self.root_path()))
        to_explore = [basepath]
        libraries = []
        folders = []
        
        # search all folders
        while len(to_explore)>0:
            path = to_explore.pop()
            if os.path.exists(path):
                for folder in glob(os.path.join(path, "*/")):
                    if folder!='/':
                        folders.append(os.path.relpath(os.path.normpath(os.path.abspath(folder)), basepath))
                        print "=>", folder 
                        if os.path.normpath(os.path.abspath(folder))!=os.path.normpath(os.path.abspath(path)):
                            to_explore.append(folder)
        
        folders.append('')
        # search for libs in folders
        for folder in folders:
            for lib in glob(os.path.join(basepath, folder, "*.lib")):
                rel_folder = os.path.relpath(os.path.normpath(os.path.abspath(lib)), basepath)
                print "=>", lib 
                folders.append(rel_folder)
                libraries.append(rel_folder)
        folders.remove('')
        print "---------------------"
        
        return libraries, folders
    
    def GetSymbols(self, library_path):
        """
        Return all symbols in a lib file
        """
        print "===> GetSymbols----"
        symbols = []
 
        path = os.path.join(self.root_path(), library_path)        
        if os.path.exists(path):
            lib_symbols = self.lib_cache.GetSymbols(library_path)
            for symbol in lib_symbols:
                symbols.append(os.path.join(library_path, symbol))
        print "----------------------"
     
        return symbols
 
    def Exists(self, path):
        return self.lib_cache.Exists(path)

    def write_library(self, library, symbols):
        with open(os.path.join(self.root_path(), library), 'w') as file:
            file.write('EESchema-LIBRARY Version 2.3\n')
            file.write('#encoding utf-8\n')

            for symbol in symbols:
                file.write(symbols[symbol].content)
            
            file.write('#\n')
            file.write('# End Library\n')
    
        dcm = re.sub(r"\.lib$", ".dcm", library)
        with open(os.path.join(self.root_path(), dcm), 'w') as file:
            file.write('EESchema-DOCLIB  Version 2.0\n')

            for symbol in symbols:
                file.write('$CMP '+symbol.replace('.mod', '')+'\n')
                file.write(symbols[symbol].text_metadata())
                file.write('\n')
                
            file.write('#\n')
            file.write('#End Doc Library\n')

    def CreateFile(self, path, content, overwrite=False):
        if self.Exists(path) and overwrite==False:
            raise KicadFileManagerException('File %s already exists'%path)

        library = re.sub(r"\.lib.*\.mod$", ".lib", path)
        symbol = re.sub(r"^.*\.lib.", "", path)
        library_path = os.path.dirname(library)
        
        fullpath = os.path.join(self.root_path(), library_path)
        if os.path.exists(fullpath)==False:
            os.makedirs(fullpath)
        
        file = rest.model.VersionedFile()
        file.source_path = path
        file.md5 = hashlib.md5(content).hexdigest()
        file.updated = rest.api.get_date()
        file.category = self.category()
        
        metadata = {}
        if file.metadata:
            metadata = json.loads(file.metadata)
        self.lib_cache.AddSymbol(path, content, metadata)
        self.write_library(library, self.lib_cache.GetSymbols(library))
        
        return file
     
    def EditFile(self, file, content, create=False):
        if self.Exists(file.source_path)==False and create==False:
            raise KicadFileManagerException('File %s does not exists'%file.source_path)
 
        library = re.sub(r"\.lib.*\.mod$", ".lib", file.source_path)
        library_path = os.path.dirname(library)

        if self.Exists(file.source_path)==True:
            symbol = self.lib_cache.GetSymbol(file.source_path)
            md5file = hashlib.md5(symbol.content).hexdigest()
            md5 = hashlib.md5(content).hexdigest()
            if md5==md5file:
                return file, False
            self.lib_cache.AddSymbol(file.source_path, content, symbol.metadata)  
            self.write_library(library, self.lib_cache.GetSymbols(library))
        else:
            self.lib_cache.AddSymbol(file.source_path, content, {})  
            self.write_library(library, self.lib_cache.GetSymbols(library))

        file.md5 = hashlib.md5(content).hexdigest()
        file.updated = rest.api.get_date()
            
        return file, True
     
    def MoveFile(self, file, dest_path, force=False):
        if self.Exists(file.source_path)==False and force==False:
            raise KicadFileManagerException('File %s does not exists'%file.source_path)
        if self.Exists(dest_path) and force==False:
            raise KicadFileManagerException('File %s already exists'%dest_path)
        
        library = re.sub(r"\.lib.*\.mod$", ".lib", file.source_path)
        library_path = os.path.dirname(library)

        symbol = self.lib_cache.GetSymbol(file.source_path)
        self.lib_cache.Clear(file.source_path)
        self.lib_cache.AddSymbol(dest_path, symbol.content, symbol.metadata)
        self.write_library(library, self.lib_cache.GetSymbols(library))
         
        file.source_path = dest_path
        file.updated = rest.api.get_date()
         
        return file
 
    def DeleteFile(self, file, force=False):
        if self.Exists(file.source_path)==False and force==False:
            raise KicadFileManagerException('File %s does not exists'%file.source_path)
        
        library = re.sub(r"\.lib.*\.mod$", ".lib", file.source_path)

        self.lib_cache.Clear(file.source_path)
        self.write_library(library, self.lib_cache.GetSymbols(library))
        
        file.updated = rest.api.get_date()
     
        return file
     
    def LoadContent(self, file):
        if self.Exists(file.source_path)==False:
            raise KicadFileManagerException('File %s does not exists'%file.source_path)
        
        file.content = self.lib_cache.GetSymbol(file.source_path).content
 
    def CreateFolder(self, path):
        abspath = os.path.join(self.root_path(), path)
        if os.path.exists(abspath):
            raise KicadFileManagerException('Folder %s already exists'%path)
        if path.endswith('.lib'):
            self.write_library(abspath, [])
        else:
            os.makedirs(abspath)
     
    def MoveFolder(self, source_path, dest_path):
        abs_source_path = os.path.join(self.root_path(), source_path)
        abs_dest_path = os.path.join(self.root_path(), dest_path)
        if os.path.exists(abs_source_path)==False:
            raise KicadFileManagerException('Folder %s does not exists'%abs_source_path)
        if os.path.exists(abs_dest_path):
            raise KicadFileManagerException('Folder %s already exists'%abs_dest_path)
        if source_path.endswith('.lib'):
            self.lib_cache.Clear(source_path)
        shutil.move(abs_source_path, abs_dest_path)
     
    def DeleteFolder(self, path):
        abspath = os.path.join(self.root_path(), path)
        if path.endswith('.lib'):
            os.remove(abspath)
        else:
            shutil.rmtree(abspath)

    def LoadMetadata(self, file):
        symbol = self.lib_cache.GetSymbol(file)
        metadata = json.loads('{}')
        if symbol:
            for meta in symbol.metadata:
                if meta=='D':
                    metadata['description'] = symbol.metadata[meta]
                else:
                    metadata[meta] = symbol.metadata[meta]
        return json.dumps(metadata)
         
    def EditMetadata(self, path, metadata):
        symbol = self.lib_cache.GetSymbol(path)
        dst_metadata = {}
        if symbol.metadata:
            dst_metadata = symbol.metadata
        src_metadata = json.loads(metadata)
        for meta in src_metadata:
            if meta=='description':
                dst_metadata['D'] = src_metadata[meta]
            else:
                dst_metadata[meta] = src_metadata[meta]                
        if len(dst_metadata)>0:
            symbol.metadata = dst_metadata
        
        library = re.sub(r"\.lib.*\.mod$", ".lib", path)
        self.write_library(library, self.lib_cache.GetSymbols(library))
        
        return metadata

