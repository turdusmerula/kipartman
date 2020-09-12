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
        self._symbols = []
        
        if os.path.exists(self.AbsPath)==False:
            self._loaded = True
            self._changed = True
        else:
            self._loaded = False
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
        if self.HasSymbol(symbol.Name):
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
                content += line
                name = line.split(' ')[1]
            elif line.startswith("ENDDEF"):
                content += line
                self._symbols.append(KicadSymbolFile(self, name, content))
                content = ''
            else:
                content += line

    def _read_metadata_file(self):
        dcm_path = re.sub(r"\.lib$", ".dcm", self.AbsPath)
        if(os.path.isfile(dcm_path)==False):
            return
 
        metadata = ''
        name = ''
        for line in open(dcm_path, 'r', encoding='utf-8'):
            line = line.replace('\n', '')
            if line.startswith("EESchema-DOCLIB"):
                pass
            elif line.startswith("#"):
                pass
            elif line.startswith("$CMP"):
                metadata += line+'\n'
                name = line.split(' ')[1]
            elif line.startswith("$ENDCMP"):
                metadata += line+'\n'
                for symbol in self._symbols:
                    if symbol.Name==name:
                        symbol._metadata = metadata
                metadata = ''
            else:
                metadata += line+'\n'
    
    def _save_lib_file(self, mtime=None):
        os.makedirs(os.path.dirname(self.AbsPath), exist_ok=True)
        with open(self.AbsPath, 'w', encoding='utf-8') as file:
            # TODO add generated from kicad
            file.write('EESchema-LIBRARY Version 2.3\n')
            file.write('#encoding utf-8\n')
 
            for symbol in self._symbols:
                file.write("#\n")
                file.write(f"# {symbol.Name}\n")
                file.write("#\n")
                file.write(symbol.Content)
             
            file.write('#\n')
            file.write('#End Library\n')

        if mtime is not None:
            # set last modification date to updated
            os.utime(self.AbsPath, (mtime, mtime))

    def _save_metadata_file(self, mtime=None):
        path = re.sub(r"\.lib$", ".dcm", self.AbsPath)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as file:
            # TODO add generated from kicad
            file.write('EESchema-DOCLIB  Version 2.0\n')
 
            for symbol in self._symbols:
                if symbol.Metadata!="":
                    file.write("#\n")
                    file.write(symbol.Metadata)
                 
            file.write('#\n')
            file.write('#End Doc Library\n')

        if mtime is not None:
            # set last modification date to updated
            os.utime(path, (mtime, mtime))

    def Save(self, mtime=None):
        def action():
            if self.Changed:
                self._save_lib_file(mtime)
                self._save_metadata_file(mtime)
            
                self._changed = False
                self._loaded = True
                for symbol in self._symbols:
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
                self.library_model.symbols.add_pending(symbolmodel)
                
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
    
    def __init__(self, owner):
        super(KicadLibraryManager, self).__init__(owner=owner, path=configuration.kicad_symbols_path) #, extensions=["lib", "dcm"])
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
                        if os.path.normpath(os.path.abspath(folder))!=os.path.normpath(os.path.abspath(path)):
                            to_explore.append(folder)
         
        folders.append('')
        # search for libs in folders
        for folder in folders:
            for lib in glob(os.path.join(basepath, folder, "*.lib")):
                rel_folder = os.path.relpath(os.path.normpath(os.path.abspath(lib)), basepath)
                libraries.append(KicadLibrary(library_file=KicadLibraryFile(rel_folder)))
        folders.remove('')

    def _load_model_libraries(self):
        libraries = KicadLibraryManager.libraries
        folders = KicadLibraryManager.folders
        
        # TODO add folders
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
