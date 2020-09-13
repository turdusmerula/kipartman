from kicad.kicad_file_manager import KicadFileManager, File, KicadFileManagerException, DELTA_FILE
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
        
        self._changed_lib = False
        self._changed_dcm = False

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
    def ChangedLib(self):
        return self._changed_lib

    @property
    def ChangedDcm(self):
        return self._changed_dcm

class KicadLibraryFile(File):
    def __init__(self, path):
        super(KicadLibraryFile, self).__init__(path)
        self._symbols = []
        
        if os.path.exists(self.AbsPath)==False:
            self._loaded_lib = True
            self._loaded_dcm = True
            self._changed_lib = True
            self._changed_dcm = True
        else:
            self._loaded_lib = False
            self._loaded_dcm = False
            self._changed_lib = False
            self._changed_dcm = False
    
    @property
    def AbsPath(self):
        return os.path.join(configuration.kicad_symbols_path, self.Path)
    
    @property
    def AbsDcmPath(self):
        return re.sub(r"\.lib$", ".dcm", self.AbsPath)
        
    @property
    def DcmPath(self):
        return re.sub(r"\.lib$", ".dcm", self.Path)

    @property
    def Symbols(self):
        self._read_lib_file()
        self._read_metadata_file()
#         if self._loaded_lib==False:
#         if self._loaded_dcm==False:
        return self._symbols

    @property
    def ChangedLib(self):
        res = self._changed_lib
        if res==False:
            for symbol in self._symbols:
                if symbol.ChangedLib:
                    return True
            return False
        return True
    
    @property
    def ChangedDcm(self):
        res = self._changed_dcm
        if res==False:
            for symbol in self._symbols:
                if symbol.ChangedDcm:
                    return True
            return False
        return True

    @property
    def MtimeLib(self):
        return os.path.getmtime(self.AbsPath)
        
    @property
    def MtimeDcm(self):
        if os.path.exists(self.AbsDcmPath):
            return os.path.getmtime(self.AbsDcmPath)
        return 0

    def HasSymbol(self, name):
        for symbol in self.Symbols:
            if symbol.Name==name:
                return True
        return False
    
    def AddSymbol(self, symbol):
        if self.HasSymbol(symbol.Name):
            raise KicadLibraryException(f"Symbol {symbol.Name} already exists in {self.Path}")
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

        self._loaded_lib = True

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
    
        self._loaded_dcm = True

    def _save_lib_file(self, mtime=None):
        log.debug(f"KicadLibraryFile._save_lib_file {self.AbsPath}")

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
        log.debug(f"KicadLibraryFile._save_metadata_file {self.AbsDcmPath}")
        os.makedirs(os.path.dirname(self.AbsDcmPath), exist_ok=True)
        with open(self.AbsDcmPath, 'w', encoding='utf-8') as file:
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
            os.utime(self.AbsDcmPath, (mtime, mtime))

    def Save(self, mtimelib=None, mtimedcm=None):
        def action():
            if self.ChangedLib:
                self._save_lib_file(mtimelib)
                self._changed_lib = False
                self._loaded_lib = True
                for symbol in self._symbols:
                    symbol._changed_lib = False
                
            if self.ChangedDcm:
                self._save_metadata_file(mtimedcm)
                self._changed_dcm = False
                self._loaded_dcm = True
                for symbol in self._symbols:
                    symbol._changed_dcm = False
                
                
        KicadFileManager.DisableNotificationsForPath(self.AbsPath, action)

    def SaveLib(self, mtimelib=None):
        def action():
            self._save_lib_file(mtimelib)
        KicadFileManager.DisableNotificationsForPath(self.AbsPath, action)

    def SaveDcm(self, mtimedcm=None):
        def action():
            self._save_metadata_file(mtimedcm)
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
    
    @property
    def Content(self):
        if self.symbol_model is not None:
            return self.symbol_model.content
        return self.symbol_file.Content

    @property
    def Description(self):
        if self.symbol_model is not None:
            return self._get_metadata(self.symbol_model.metadata, "D")
        return self._get_metadata(self.symbol_file.Metadata, "D")
    
    def _synchronize(self):
        file_changed = False
        model_changed = False
        
        if self.symbol_file is None and self.symbol_model is not None:
            # symbol exists in database but not in file
            self._symbol_file = KicadSymbolFile(self._library.library_file, self.symbol_model.name, self.symbol_model.content, self.symbol_model.metadata)
            self._symbol_file._changed_lib = True
            self._symbol_file._changed_dcm = True
            self._library.library_file.AddSymbol(self._symbol_file)
            file_changed = True
            log.info(f"added '{self.Name}' symbol in '{self._library.library_file.Path}' from database")
        elif self.symbol_file is not None and self.symbol_model is None:
            # symbol exists in file but not in database
            self.symbol_model = api.data.library_symbol.create()
            self.symbol_model.library = self._library.library_model
            self.symbol_model.name = self.symbol_file.Name
            self.symbol_model.content = self.symbol_file.Content
            self.symbol_model.metadata = self.symbol_file.Metadata
            self._library.library_model.symbols.add_pending(self.symbol_model)
            model_changed = True
            log.info(f"added '{self.Name}' symbol in database from '{self._library.library_file.Path}'")
        else:
            delta = self._library.library_file.MtimeLib-self._library.library_model.mtime_lib

            if delta<=-DELTA_FILE:
                # database is newer than file
                self.symbol_file._content = self.symbol_model.content
                self.symbol_file._changed_lib = True
                file_changed = True
                log.info(f"changed '{self.Name}' symbol in '{self._library.library_file.Path}' from database")
            elif delta>=DELTA_FILE:
                # file is newer than database
                self.symbol_model.content = self.symbol_file._content
                self._library.library_model.symbols.add_pending(self.symbol_model)
                model_changed = True
                log.info(f"changed '{self.Name}' in database from '{self._library.library_file.Path}'")

            delta = self._library.library_file.MtimeDcm-self._library.library_model.mtime_dcm

            if delta<=-DELTA_FILE:
                # database is newer than file
                self.symbol_file._metadata = self.symbol_model.metadata
                self.symbol_file._changed_dcm = True
                file_changed = True
                log.info(f"changed '{self.Name}' symbol in '{self._library.library_file.DcmPath}' from database")
            elif delta>=DELTA_FILE:
                # file is newer than database
                self.symbol_model.metadata = self.symbol_file._metadata
                self._library.library_model.symbols.add_pending(self.symbol_model)
                model_changed = True
                log.info(f"changed '{self.Name}' in database from '{self._library.library_file.DcmPath}'")

        return (file_changed, model_changed)
    
    def _get_metadata(self, metadata, field):
        if metadata is None:
            return ''
        
        for line in metadata.split('\n'):
            line = re.sub(r"\n$", "", line)
            if line.startswith(f"{field} "):
                return re.sub(f"^{field} ", "", line)
        
        return ''
    
class KicadLibrary():
    """
    This object is the bridge between library file and library record in database
    """
    
    def __init__(self, library_file=None, library_model=None):
        self.library_file = library_file
        self.library_model = library_model
        
        self._symbols = []
    
    @property
    def AbsPath(self):
        if self.library_model is not None:
            return os.path.join(configuration.kicad_symbols_path, self.library_model.path)
        return self.library_file.AbsPath
    
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

    def _library_file_to_model(self, library_file, library_model=None):
        if library_model is None:
            library_model = api.data.library.create()
    
        # fill library_model fields
        library_model.path = library_file.Path
        library_model.mtime_lib = self.library_file.MtimeLib
        library_model.mtime_dcm = self.library_file.MtimeDcm
        
        # fill symbols
        for symbolfile in library_file.Symbols:
            symbolmodel = None
            for s in library_model.symbols.all():
                if s.name==symbolfile.Name:
                    symbolmodel = s
            
            if symbolmodel is None:
                symbolmodel = api.data.library_symbol.create()
            
            # fill symbol fiels
            symbolmodel.name = symbolfile.Name
            symbolmodel.content = symbolfile.Content
            symbolmodel.metadata = symbolfile.Metadata
            
            library_model.symbols.add_pending(symbolmodel)
        
        return library_model
        
    def _library_model_to_file(self, library_model, library_file=None):
        if library_file is None:
            # create it on disk
            library_file = KicadLibraryFile(path=library_model.path)

        # add symbols
        for symbolmodel in self.library_model.symbols.all():
            symbolfile = None
            for s in library_model._symbols:
                if s.Name==symbolmodel.name:
                    symbolfile = s
            
            if symbolfile is None:
                symbolfile = KicadSymbolFile(library_file, symbolmodel.name, symbolmodel.content, symbolmodel.metadata)

            library_file.AddSymbol(symbolfile)

        return library_file
    
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
            
            self.library_file.Save(self.library_model.mtime_lib, self.library_model.mtime_dcm)
            log.info(f"created file {self.library_file.path}")
            
        elif self.library_file is not None and self.library_model is None:
            # library exists on disk but not in database
            self.library_model = self._library_file_to_model(self.library_file)
            api.data.library.save(self.library_model)
            log.info(f"imported file {self.library_file.path} in database")
        
        # at this point both library_file and library_model are presents
        
        file_changed = False
        model_changed = False
        for symbol in self._symbols:
            fc, mc = symbol._synchronize()
            if fc:
                file_changed = True
            if mc:
                model_changed = True

        if file_changed:
            self.library_file.Save()
            model_changed = True
            log.info(f"updated file {self.library_file.path}")

        if model_changed:
            self.library_model.mtime_lib = self.library_file.MtimeLib
            self.library_model.mtime_dcm = self.library_file.MtimeDcm
            api.data.library.save(self.library_model)
            log.info(f"updated database for {self.library_model.path}")
            
    def __repr__(self):
        res = "<KicadLibrary> ("
        if self.library_file:
            res += f"file={self.library_file.Path} "
        if self.library_model:
            res += f"model={self.library_model.Path}"
        res += ")"
        return res
    
class KicadLibraryManager(KicadFileManager):
    libraries = []
    folders = []
    loaded = False
    
    def __init__(self, owner):
        super(KicadLibraryManager, self).__init__(owner=owner, path=configuration.kicad_symbols_path) #, extensions=["lib", "dcm"])

    def Reload(self):
        KicadLibraryManager.loaded = False
        self._load()
        
    def _load(self):
        if KicadLibraryManager.loaded==False:
            self._load_file_libraries()
            self._load_model_libraries()
        KicadLibraryManager.loaded = True
        
    def _load_file_libraries(self):
        """
        Recurse all folders to find lib files
        """
        log.debug(f"KicadLibraryManager._load_file_libraries")
        
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
        log.debug(f"KicadLibraryManager._load_model_libraries")

        libraries = KicadLibraryManager.libraries
        folders = KicadLibraryManager.folders
        
        for library in api.data.library.find():
            libraryset = self._find_library(library.path)
            if libraryset is None:
                libraryset = KicadLibrary(library_model=library)
                libraries.append(libraryset)
            else:
                libraryset.library_model = library
    
            # add folders
            pathel = self._cut_path(os.path.dirname(library.path))
            path = ''
            for el in pathel:
                path = os.path.join(path, el)
                if path not in folders:
                    folders.append(path)
            
    def _cut_path(self, path):
        res = []
        while len(path)>0:
            path, folder = os.path.split(path)
            res.append(folder)
        res.reverse()
    
        if len(res)==1 and res[0]=='.':
            return []
        return res

            
    def _find_library(self, path):
        for library in KicadLibraryManager.libraries:
            if library.Path==path:
                return library
        return None
    
    def _add_folder(self, path):
        # TODO
        pass

    def _on_change_prehook(self, path):
#         if path.endswith(".lib") or path.endswith(".dcm") :
        KicadLibraryManager.loaded = False
        return True
        
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
        os.makedirs(abspath)
        
    def MoveFolder(self, path, newpath):
        abspath = os.path.join(configuration.kicad_symbols_path, path)
        if os.path.exists(abspath)==False:
            raise KicadFileManagerException(f"Folder '{path}' does not exists")
        newabspath = os.path.join(configuration.kicad_symbols_path, newpath)
        if os.path.exists(newabspath):
            raise KicadFileManagerException(f"Folder '{newpath}' already exists")
        
        # move files
        def action():
            os.makedirs(os.path.dirname(abspath), exist_ok=True)
            os.rename(abspath, newabspath)
        self.DisableNotificationsForPath(configuration.kicad_symbols_path, action=action)
        log.info(f"moved folder '{abspath}' to '{newabspath}'")
        
        # edit database
        libraries = api.data.library.find()
        for library in libraries:
            if library.path.startswith(path+os.sep):
                previous_path = library.path
                library.path = re.sub(f"^{path}", f"{newpath}", library.path)
                api.data.library.save(library)
                log.info(f"moved library '{previous_path}' to '{library.path}'")
        
    def CreateLibrary(self, path):
        abspath = os.path.join(configuration.kicad_symbols_path, path)
        if os.path.exists(abspath):
            raise KicadFileManagerException(f"Library '{path}' already exists")
        
        library_file = KicadLibraryFile(path)
        self.DisableNotificationsForPath(configuration.kicad_symbols_path, action=library_file.Save)
        
        library = KicadLibrary(library_file)
        
        KicadLibraryManager.libraries.append(library)

        return library

    def MoveLibrary(self, library, newpath):
        previousname = library.Path
        newname = os.path.basename(newpath)
        newpath = os.path.dirname(newpath)
        newabspath = os.path.join(configuration.kicad_symbols_path, newpath)
        
        if os.path.exists(newabspath)==False:
            raise KicadFileManagerException(f"Folder '{newpath}' does not exists")
        if newname.endswith(".lib")==False:
            raise KicadFileManagerException(f"'{newname}' is not a valid library name")
        
        def action():
            os.rename(library.AbsPath, os.path.join(newabspath, newname))
        self.DisableNotificationsForPath(configuration.kicad_symbols_path, action=action)
        
        library.library_model.path = os.path.join(newpath, newname)
        api.data.library.save(library.library_model)
        
        log.info(f"library '{previousname}' renamed to '{os.path.join(newpath, newname)}'")

        return library
    
    def DeleteLibrary(self, library):
        symbols_to_remove = []
        for symbol in library.Symbols:
            symbols_to_remove.append(symbol.symbol_model)
        
        associated_parts = api.data.part.find([api.data.part.FilterSymbols(symbols_to_remove)])
        for associated_part in associated_parts:
            log.info(f"part '{associated_part.name} dissociated from {associated_part.symbol.name}")
            associated_part.symbol = None
            associated_part.save()
        
        library.library_model.delete()
        def action():
            os.remove(library.AbsPath)
        self.DisableNotificationsForPath(configuration.kicad_symbols_path, action=action)

        log.info(f"library '{library.Path}' removed")

    def DeleteFolder(self, path):
#         if len(os.listdir(os.path.join(configuration.kicad_symbols_path, path)))>0:
#             raise KicadFileManagerException(f"Folder '{path}' is not empty")
        def action():
            shutil.rmtree(os.path.join(configuration.kicad_symbols_path, path))
        self.DisableNotificationsForPath(configuration.kicad_symbols_path, action=action)

        log.info(f"folder '{path}' removed")
        