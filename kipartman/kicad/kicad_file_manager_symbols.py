from kicad.kicad_file_manager import KicadFileManager, File, KicadFileManagerException
from configuration import configuration
from glob import glob
import os
import re
import shutil
from helper.log import log
from helper.exception import print_callstack
import api.models
import api.data
import helper.date
import math

def cut_path(path):
    res = []
    while len(path)>0:
        path, folder = os.path.split(path)
        res.append(folder)
    res.reverse()

    if len(res)==1 and res[0]=='.':
        return []
    return res

class KicadLibraryException(Exception):
    def __init__(self, error):
        super(KicadLibraryException, self).__init__(error)

class KicadSymbolFile():
    def __init__(self, library, name, content, metadata=""):
        self._library = library
        self._name = name
        self._content = content
        self._metadata = metadata
        
        self._changed = False

    @property
    def Library(self):
        return self._library
    
    @property
    def Name(self):
        return self._name
    
    @property
    def Content(self):
        return self._content

    @property
    def Metadata(self):
        return self._metadata
    
    @property
    def Changed(self):
        return self._changed

class KicadLibraryFile(File):
    def __init__(self, path):
        super(KicadLibraryFile, self).__init__(path)
        self._loaded = False
        self._symbols = []
        
        if os.path.exists(self.AbsPath)==False:
            self._changed = True
        else:
            self._changed = False
    
    @property
    def AbsPath(self):
        return os.path.join(configuration.kicad_symbols_path, self.Path)
    
    @property
    def Symbols(self):
        if self._loaded==False:
            self._read_lib_file()
            self._read_metadata_file()
        return self._symbols

    @property
    def Changed(self):
        res = self._changed
        if self._changed==False:
            for symbol in self._symbols:
                if symbol.Changed:
                    return True
            return False
        return True
    
    @property
    def Mtime(self):
        # TODO
        return os.path.getmtime(self.AbsPath)
        
    def HasSymbol(self, name):
        for symbol in self.Symbols:
            if symbol.Name==name:
                return True
        return False
    
    def AddSymbol(self, symbol):
        if self.HasSymbol(symbol.name):
            raise KicadLibraryException(f"Symbol {symbol.name} already exists in {self.Path}")
        self._symbols.append(symbol)
        symbol._library = self
        self._changed = True
        
    def RemoveSymbol(self, symbol):
        if self.HasSymbol(symbol.name)==False:
            raise KicadLibraryException(f"Symbol {symbol.name} does not exists in {self.Path}")
        for s in self._symbols:
            if s.Name==symbol.Name:
                self._symbols.remove(s)
                break
        self._changed = True

    def _read_lib_file(self):
        self._symbols = []
        if(os.path.isfile(self.AbsPath)==False):
            return
 
        content = ''
        name = ''
        for line in open(self.AbsPath, 'r', encoding='utf-8'):
            if line.startswith("EESchema-LIBRARY"):
                pass
            elif line.startswith("#encoding"):
                pass
            elif line.startswith("#"):
                pass
                #content = content+line
            elif line.startswith("DEF"):
                content = content+line
                name = line.split(' ')[1]
            elif line.startswith("ENDDEF"):
                content = content+line
                self._symbols.append(KicadSymbolFile(self, name, content))
                content = ''
            else:
                content = content+line

    def _read_metadata_file(self):
        dcm_path = re.sub(r"\.lib$", ".dcm", self.AbsPath)
        if(os.path.isfile(dcm_path)==False):
            return
 
        name = ''
        for line in open(dcm_path, 'r'):
            line = line.replace('\n', '')
            if line.startswith("EESchema-DOCLIB"):
                pass
            elif line.startswith("#"):
                pass
            elif line.startswith("$CMP"):
                name = line.split(' ')[1]+'.mod'
            elif line.startswith("$ENDCMP"):
                name = ''
            elif name!='':
                label = line.split(' ')[0]
                value = " ".join(line.split(' ')[1:])
                for symbol in self._symbols:
                    if symbol.Name==name:
                        symbol._metadata = value
    
    def _save_lib_file(self, mtime=None):
        with open(self.AbsPath, 'w', encoding='utf-8') as file:
            file.write('EESchema-LIBRARY Version 2.3\n')
            file.write('#encoding utf-8\n')
 
            for symbol in self._symbols:
                file.write(symbol.Content)
             
            file.write('#\n')
            file.write('# End Library\n')

            if mtime is not None:
                # set last modification date to updated
#                 utimeupdated = helper.date.datetime_to_utime(updated)
                os.utime(self.AbsPath, (mtime, mtime))

    def _save_metadata_file(self, mtime=None):
        path = re.sub(r"\.lib$", ".dcm", self.AbsPath)
        with open(path, 'w', encoding='utf-8') as file:
            file.write('EESchema-DOCLIB  Version 2.0\n')
 
            for symbol in self._symbols:
                file.write(f'$CMP {symbol.Name}\n')
                file.write(symbol.Metadata)
                file.write('\n')
                 
            file.write('#\n')
            file.write('#End Doc Library\n')

        if mtime is not None:
            # set last modification date to updated
#             utimeupdated = helper.date.datetime_to_utime(updated)
            os.utime(path, (mtime, mtime))

    def Save(self, mtime=None):
        def action():
            if self.Changed:
                self._save_lib_file(mtime)
                self._save_metadata_file(mtime)
            
                self._changed = False
                for symbol in self.Symbols:
                    symbol._changed = False
                
        KicadFileManager.DisableNotificationsForPath(self.AbsPath, action)

class KicadSymbol():
    """
    This object is the bridge between symbol in library file and symbol record in database
    """
    
    def __init__(self, library, symbol_file=None, symbol_model=None):
        self.symbol_file = symbol_file
        self.symbol_model = symbol_model
        self._library = library
    
    @property
    def Library(self):
        return self._library
     
    @property
    def Name(self):
        if self.symbol_model is not None:
            return self.symbol_model.name
        return self.symbol_file.Name
    
    def _synchronize(self):
        delta = self._library.library_file.Mtime-self._library.library_model.mtime
        if delta<=-0.0001:
            # database is newer than file
            log.info(f"changed {self.Name} in file")
        elif delta>=0.0001:
            # file is newer than database
            if self.symbol_model is None:
                self.symbol_model = api.data.library_symbol.create()
                
            self.symbol_model.library = self._library.library_model
            self.symbol_model.name = self.symbol_file.Name
            self.symbol_model.content = self.symbol_file.Content
            self.symbol_model.metadata = self.symbol_file.Metadata
            
            self._library.library_model.symbols.add_pending(self.symbol_model)
            log.info(f"changed {self.Name} in database")
        else:
            # no changes found, nothing to do
            pass
    
class KicadLibrary():
    """
    This object is the bridge between library file and library record in database
    """
    
    def __init__(self, library_file=None, library_model=None):
        self.library_file = library_file
        self.library_model = library_model
        
        self._symbols = []
     
    @property
    def Path(self):
        if self.library_model is not None:
            return self.library_model.path
        return self.library_file.Path

    @property
    def Symbols(self):
        self._load_symbols()
        return self._symbols
    
    def _load_symbols(self):
        self._symbols = []
        
        if self.library_file is not None:
            for symbol in self.library_file.Symbols:
                self._symbols.append(KicadSymbol(library=self, symbol_file=symbol))
        
        if self.library_model is not None:
            for symbol in self.library_model.symbols.all():
                symbolset = self._find_symbol(symbol.name)
                if symbolset is None:
                    symbolset = KicadSymbol(library=self, symbol_model=symbol)
                    self._symbols.append(symbolset)
                else:
                    symbolset.symbol_model = symbol
                    
        self._synchronize()

    def _find_symbol(self, name):
        for symbol in self._symbols:
            if symbol.Name==name:
                return symbol

    def _synchronize(self):
        """
        synchronize file and database
        """
        if self.library_file is None and self.library_model is not None:
            # library exists in database but not on disk
            # create it on disk
            self.library_file = KicadLibraryFile(path=self.library_model.path)

            # add symbols
            for symbolmodel in self.library_model.symbols.all():
                symbolfile = KicadSymbolFile(self.library_file, symbolmodel.name, symbolmodel.content, symbolmodel.metadata)
                self.library_file.AddSymbol(symbolfile)
            
            self.library_file.Save(self.library_model.mtime)
            log.info(f"created file {self.library_file.path}")
        elif self.library_file is not None and self.library_model is None:
            # library exists on disk but not in database
            # create it on database
            self.library_model = api.data.library.create()
            self.library_model.path = self.library_file.Path
            
            # add symbols
            for symbolfile in self.library_file.Symbols:
                symbolmodel = api.data.library_symbol.create()
                symbolmodel.name = symbolfile.Name
                symbolmodel.content = symbolfile.Content
                symbolmodel.metadata = symbolfile.Metadata
                self.library_model.add_pending(symbolmodel)
                
            self.library_model.mtime = self.library_file.Mtime
            api.data.library.save(self.library_model)
            log.info(f"imported file {self.library_file.path}")
        elif math.fabs(self.library_model.mtime!=self.library_file.Mtime)>=0.0001:
            self.library_model.mtime = self.library_file.Mtime
            
            # file and database exists
            for symbol in self._symbols:
                symbol._synchronize()
            api.data.library.save(self.library_model)
            self.library_file.Save(self.library_model.mtime)
            log.info(f"synchronized file {self.library_file.path}")

class KicadLibraryManager(KicadFileManager):
    libraries = []
    folders = []
    loaded = False
    
    def __init__(self):
        super(KicadLibraryManager, self).__init__(watch_path=configuration.kicad_symbols_path, extensions=["lib", "dcm"])
        self._loaded = False
        
    def _load(self):
        if KicadLibraryManager.loaded==False:
            self._load_file_libraries()
            self._load_model_libraries()
        KicadLibraryManager.loaded = True
        
    def _load_file_libraries(self):
        """
        Recurse all folders to find lib files
        """
        libraries = KicadLibraryManager.libraries
        folders = KicadLibraryManager.folders
        
        libraries.clear()
        folders.clear()
        
        basepath = os.path.normpath(os.path.abspath(configuration.kicad_symbols_path))
        to_explore = [basepath]
         
        # search all folders
        while len(to_explore)>0:
            path = to_explore.pop()
            if os.path.exists(path):
                for folder in glob(os.path.join(path, "*/")):
                    if folder!='/':
                        folders.append(os.path.relpath(os.path.normpath(os.path.abspath(folder)), basepath))
                        #print("=>", folder) 
                        if os.path.normpath(os.path.abspath(folder))!=os.path.normpath(os.path.abspath(path)):
                            to_explore.append(folder)
         
        folders.append('')
        # search for libs in folders
        for folder in folders:
            for lib in glob(os.path.join(basepath, folder, "*.lib")):
                rel_folder = os.path.relpath(os.path.normpath(os.path.abspath(lib)), basepath)
                #print("=>", lib) 
#                 folders.append(rel_folder)
                libraries.append(KicadLibrary(library_file=KicadLibraryFile(rel_folder)))
        folders.remove('')

    def _load_model_libraries(self):
        libraries = KicadLibraryManager.libraries
        folders = KicadLibraryManager.folders
        
        for library in api.data.library.find():
            libraryset = self._find_library(library.path)
            if libraryset is None:
                libraryset = KicadLibrary(library_model=library)
                libraries.append(libraryset)
            else:
                libraryset.library_model = library
            
    def _find_library(self, path):
        for library in KicadLibraryManager.libraries:
            if library.Path==path:
                return library
        return None
    
    def _add_folder(self, path):
        # TODO
        pass

    @property
    def Libraries(self):
        self._load()
        return KicadLibraryManager.libraries

    @property
    def Folders(self):
        self._load()
        return KicadLibraryManager.folders

    def CreateFolder(self, path):
        abspath = os.path.join(configuration.kicad_symbols_path, path)
        if os.path.exists(abspath):
            raise KicadFileManagerException(f"Folder '{path}' already exists")
        super(KicadLibraryManager, self).CreateFolder(abspath)
      
    def CreateLibrary(self, path):
        abspath = os.path.join(configuration.kicad_symbols_path, path)
        if os.path.exists(abspath):
            raise KicadFileManagerException(f"Library '{path}' already exists")
        
        library = KicadLibrary(path)
        KicadLibraryManager.libraries.append(library)
        library._changed = True
        return library
    

#         
#     def Clear(self, path=None):
#         if path:
#             if path.endswith('.lib'):
#                 if path in self.libs:
#                     self.libs.pop(path)
#             elif path.endswith('.mod'):
#                 library = re.sub(r"\.lib.*\.mod$", ".lib", path)
#                 symbol = re.sub(r"^.*\.lib.", "", path)
#                 if library in self.libs and symbol in self.libs[library]:
#                     self.libs[library].pop(symbol)
#         else:
#             self.libs = {}
#         
#     def GetSymbol(self, symbol_path):
#         library = re.sub(r"\.lib.*\.mod$", ".lib", symbol_path)
#         symbol = re.sub(r"^.*\.lib.", "", symbol_path)
# 
#         if library in self.libs and symbol in self.libs[library]:
#             return self.libs[library][symbol]
#         else:
#             symbols = self.read_lib_file(library)
#             metadata = self.read_metadata_file(library)
#             self.libs[library] = {}
#             for symbol in symbols:
#                 if symbol in metadata:
#                     meta = metadata[symbol]
#                 #print("%$$$", meta)
#                 self.libs[library][symbol] = KicadLibCacheElement(content=symbols[symbol], metadata=meta)
# 
#         if library in self.libs and symbol in self.libs[library]:
#             return self.libs[library][symbol]
#         return None
#         
#     def GetSymbols(self, lib_path):
#         if lib_path in self.libs:
#             return self.libs[lib_path]
#         else:
#             symbols = self.read_lib_file(lib_path)
#             metadata = self.read_metadata_file(lib_path)
#             self.libs[lib_path] = {}
#             for symbol in symbols:
#                 meta = {}
#                 if metadata and symbol in metadata:
#                     meta = metadata[symbol]
#                 #print("%$$$", symbol, meta)
#                 self.libs[lib_path][symbol] = KicadLibCacheElement(content=symbols[symbol], metadata=meta)
#         
#         if lib_path in self.libs:
#             return self.libs[lib_path]
#         return {}
#     
#     def update_content(self, name, content):
#         new_content = ''
#         has_def = False
#         for line in content.split('\n'):
#             if line.startswith('#'):
#                 pass
#             elif line.startswith('DEF'):
#                 els = line.split(' ')
#                 els[1] = name
#                 if new_content!='':
#                     new_content = new_content+'\n'
#                 new_content = new_content+" ".join(els)
#                 has_def = True
#             else:
#                 if new_content!='':
#                     new_content = new_content+'\n'
#                 new_content = new_content+line
# #        content = "#\n"+content    
# #        content = "# "+name+'\n'+content    
# #        content = "#\n"+content    
# 
#         if has_def==False:
#             new_content = new_content+"DEF "+name+" RF 0 40 Y N 1 F N\n"
#             new_content = new_content+"DRAW\n"
#             new_content = new_content+"ENDDRAW\n"
#             new_content = new_content+"ENDDEF\n"
#             
#         return new_content
#     
#     def AddSymbol(self, path, content, metadata):
#         library = re.sub(r"\.lib.*\.mod$", ".lib", path)
#         symbol = re.sub(r"^.*\.lib.", "", path)
#         symbol_name = re.sub(r".mod$", "", os.path.basename(path))
#         
#         content = self.update_content(symbol_name, content)
#         if library not in self.libs:
#             self.libs[library] = {}
#         self.libs[library][symbol] = KicadLibCacheElement(content, metadata)
#         
#     def Exists(self, path):
#         if path.endswith('.mod'):
#             library = re.sub(r"\.lib.*\.mod$", ".lib", path)
#             symbol = re.sub(r"^.*\.lib.", "", path)
#             
#             symbols = self.GetSymbols(library)
#             if symbols and symbol in symbols:
#                 return True
#             return False
#         elif path.endswith('.lib'):
#             if self.GetSymbols(path):
#                 return True
#             return False
#         else:
#             return os.path.exists(os.path.join(self.root_path, path))

# def replace_last(source_string, replace_what, replace_with):
#     head, _sep, tail = source_string.rpartition(replace_what)
#     return head + replace_with + tail
# 
# class KicadLibCacheElement(object):
#     def __init__(self, content='', metadata={}):
#         self.content = content
#         self.metadata = metadata
# 
#     def text_metadata(self):
#         res = ''
#         for metadata in self.metadata:
#             if metadata=='K' or metadata=='D':
#                 if res!='':
#                     res = res+'\n'
#                 res = res+metadata+' '+self.metadata[metadata]
#         return res
# 
#    
#         
# class KicadFileManagerLib(KicadFileManager):
#     """
#     Simulate lib files as a folder containing symbol files
#     """
#     def __init__(self):
#         super(KicadFileManagerLib, self).__init__()
#         self.lib_cache = KicadLibCache(self.root_path())
#         self.extensions = ['lib', 'dcm']
# 
#     def root_path(self):
#         return configuration.kicad_symbols_path
# 
#     def on_change_prehook(self, path):
# # #         # discard cache
# #         if path.endswith(".dcm"):
# #             self.lib_cache.Clear(re.sub(r"\.dcm$", ".lib", path))
# #         if path.endswith(".lib"):
# #             self.lib_cache.Clear(path)
#         pass
#     
#     def Load(self):
#         """
#         fill cache files from disk
#         """
#         self.files = {}
#         libraries, self.folders = self.GetLibraries()
#         self.lib_cache.Clear()
#         
#         for library in libraries:
#             symbols = self.GetSymbols(library)
#             for symbol in symbols:
#                 file = File()
#                 file.source_path = symbol
#                 self.LoadContent(file)
#                 file.md5 = hash.md5(file.content).hexdigest()
#                 file.category = self.category()
#                 file.metadata = self.LoadMetadata(symbol)
#                 
#                 self.files[file.source_path] = file
#     
#     def write_library(self, library, symbols):
#         with open(os.path.join(self.root_path(), library), 'w', encoding='utf-8') as file:
#             file.write('EESchema-LIBRARY Version 2.3\n')
#             file.write('#encoding utf-8\n')
# 
#             for symbol in symbols:
#                 file.write(symbols[symbol].content)
#             
#             file.write('#\n')
#             file.write('# End Library\n')
#     
#         dcm = re.sub(r"\.lib$", ".dcm", library)
#         with open(os.path.join(self.root_path(), dcm), 'w', encoding='utf-8') as file:
#             file.write('EESchema-DOCLIB  Version 2.0\n')
# 
#             for symbol in symbols:
#                 file.write('$CMP '+symbol.replace('.mod', '')+'\n')
#                 file.write(symbols[symbol].text_metadata())
#                 file.write('\n')
#                 
#             file.write('#\n')
#             file.write('#End Doc Library\n')
# 
#     def CreateFile(self, path, content, overwrite=False):
#         if self.Exists(path) and overwrite==False:
#             raise KicadFileManagerException('File %s already exists'%path)
# 
#         library = re.sub(r"\.lib.*\.mod$", ".lib", path)
#         symbol = re.sub(r"^.*\.lib.", "", path)
#         library_path = os.path.dirname(library)
#         
#         fullpath = os.path.join(self.root_path(), library_path)
#         if os.path.exists(fullpath)==False:
#             os.makedirs(fullpath)
#         
#         file = File()
#         file.source_path = path
#         file.md5 = hash.md5(content).hexdigest()
#         file.updated = rest.api.get_date()
#         file.category = self.category()
#         
#         metadata = {}
#         if file.metadata:
#             metadata = json.loads(file.metadata)
#         self.lib_cache.AddSymbol(path, content, metadata)
#         self.write_library(library, self.lib_cache.GetSymbols(library))
#         
#         return file
#      
#     def EditFile(self, file, content, create=False):
#         if self.Exists(file.source_path)==False and create==False:
#             raise KicadFileManagerException('File %s does not exists'%file.source_path)
#  
#         library = re.sub(r"\.lib.*\.mod$", ".lib", file.source_path)
#         library_path = os.path.dirname(library)
# 
#         if self.Exists(file.source_path)==True:
#             symbol = self.lib_cache.GetSymbol(file.source_path)
#             md5file = hash.md5(symbol.content).hexdigest()
#             md5 = hash.md5(content).hexdigest()
#             if md5==md5file:
#                 return file, False
#             self.lib_cache.AddSymbol(file.source_path, content, symbol.metadata)  
#             self.write_library(library, self.lib_cache.GetSymbols(library))
#         else:
#             self.lib_cache.AddSymbol(file.source_path, content, {})  
#             self.write_library(library, self.lib_cache.GetSymbols(library))
# 
#         file.md5 = hash.md5(content).hexdigest()
#         file.updated = rest.api.get_date()
#             
#         return file, True
#      
#     def MoveFile(self, file, dest_path, force=False):
#         if self.Exists(file.source_path)==False and force==False:
#             raise KicadFileManagerException('File %s does not exists'%file.source_path)
#         if self.Exists(dest_path) and force==False:
#             raise KicadFileManagerException('File %s already exists'%dest_path)
#         
#         library = re.sub(r"\.lib.*\.mod$", ".lib", file.source_path)
#         library_path = os.path.dirname(library)
# 
#         symbol = self.lib_cache.GetSymbol(file.source_path)
#         self.lib_cache.Clear(file.source_path)
#         self.lib_cache.AddSymbol(dest_path, symbol.content, symbol.metadata)
#         self.write_library(library, self.lib_cache.GetSymbols(library))
#          
#         file.source_path = dest_path
#         file.updated = rest.api.get_date()
#          
#         return file
#  
#     def DeleteFile(self, file, force=False):
#         if self.Exists(file.source_path)==False and force==False:
#             raise KicadFileManagerException('File %s does not exists'%file.source_path)
#         
#         library = re.sub(r"\.lib.*\.mod$", ".lib", file.source_path)
# 
#         self.lib_cache.Clear(file.source_path)
#         self.write_library(library, self.lib_cache.GetSymbols(library))
#         
#         file.updated = rest.api.get_date()
#      
#         return file
#      
#     def LoadContent(self, file):
#         if self.Exists(file.source_path)==False:
#             raise KicadFileManagerException('File %s does not exists'%file.source_path)
#         
#         file.content = self.lib_cache.GetSymbol(file.source_path).content
#  
#     def MoveFolder(self, source_path, dest_path):
#         abs_source_path = os.path.join(self.root_path(), source_path)
#         abs_dest_path = os.path.join(self.root_path(), dest_path)
#         if os.path.exists(abs_source_path)==False:
#             raise KicadFileManagerException('Folder %s does not exists'%abs_source_path)
#         if os.path.exists(abs_dest_path):
#             raise KicadFileManagerException('Folder %s already exists'%abs_dest_path)
#         if source_path.endswith('.lib'):
#             self.lib_cache.Clear(source_path)
#         shutil.move(abs_source_path, abs_dest_path)
#      
#     def DeleteFolder(self, path):
#         abspath = os.path.join(self.root_path(), path)
#         if path.endswith('.lib'):
#             os.remove(abspath)
#         else:
#             shutil.rmtree(abspath)
# 
#     def LoadMetadata(self, file):
#         symbol = self.lib_cache.GetSymbol(file)
#         metadata = json.loads('{}')
#         if symbol:
#             for meta in symbol.metadata:
#                 if meta=='D':
#                     metadata['description'] = symbol.metadata[meta]
#                 else:
#                     metadata[meta] = symbol.metadata[meta]
#         return json.dumps(metadata)
#          
#     def EditMetadata(self, path, metadata):
#         symbol = self.lib_cache.GetSymbol(path)
#         dst_metadata = {}
#         if symbol.metadata:
#             dst_metadata = symbol.metadata
#         src_metadata = json.loads(metadata)
#         for meta in src_metadata:
#             if meta=='description':
#                 dst_metadata['D'] = src_metadata[meta]
#             else:
#                 dst_metadata[meta] = src_metadata[meta]                
#         if len(dst_metadata)>0:
#             symbol.metadata = dst_metadata
#         
#         library = re.sub(r"\.lib.*\.mod$", ".lib", path)
#         self.write_library(library, self.lib_cache.GetSymbols(library))
#         
#         return metadata
