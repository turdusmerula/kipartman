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

class KicadSymbolLibraryException(Exception):
    def __init__(self, error):
        super(KicadSymbolLibraryException, self).__init__(error)

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

#     def _
class KicadSymbolLibraryFile(File):
    def __init__(self, path):
        super(KicadSymbolLibraryFile, self).__init__(path)
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
    
        self._read_lib_file()
        self._read_metadata_file()
    
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
            raise KicadSymbolLibraryException(f"Symbol {symbol.Name} already exists in {self.Path}")
        self._symbols.append(symbol)
        symbol._library = self
        self._changed = True
        
    def RemoveSymbol(self, symbol):
        if self.HasSymbol(symbol.name)==False:
            raise KicadSymbolLibraryException(f"Symbol {symbol.name} does not exists in {self.Path}")
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
                
                dup = ""
                dupn = 1
                for symbol in self._symbols:
                    if symbol.Name==name+dup:
                        dup = f"_{dupn}"
                        dupn += 1
                if dup!="":
                    log.info(f"duplication found in '{self.Path}', renamed to '{name+dup}'")
                    
                self._symbols.append(KicadSymbolFile(self, name+dup, content))
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
        log.debug(f"KicadSymbolLibraryFile._save_lib_file {self.AbsPath}")

        os.makedirs(os.path.dirname(self.AbsPath), exist_ok=True)
        with open(self.AbsPath, 'w', encoding='utf-8') as file:
            # TODO add generated from kicad
            file.write('EESchema-LIBRARY Version 2.3\n')
            file.write('#encoding utf-8\n')
 
            for symbol in self._symbols:
                file.write("#\n")
                file.write(f"# {symbol.Name}\n")
                file.write("#\n")
                file.write(self._format_content(symbol, symbol.Content))
             
            file.write('#\n')
            file.write('#End Library\n')

        if mtime is not None:
            # set last modification date to updated
            os.utime(self.AbsPath, (mtime, mtime))

    def _save_metadata_file(self, mtime=None):
        log.debug(f"KicadSymbolLibraryFile._save_metadata_file {self.AbsDcmPath}")
        os.makedirs(os.path.dirname(self.AbsDcmPath), exist_ok=True)
        with open(self.AbsDcmPath, 'w', encoding='utf-8') as file:
            # TODO add generated from kicad
            file.write('EESchema-DOCLIB  Version 2.0\n')
 
            for symbol in self._symbols:
                if symbol.Metadata!="":
                    file.write("#\n")
                    file.write(self._format_metadata(symbol, symbol.Metadata))
                 
            file.write('#\n')
            file.write('#End Doc Library\n')

        if mtime is not None:
            # set last modification date to updated
            os.utime(self.AbsDcmPath, (mtime, mtime))

    def _set_metadata_field(self, metadata, field, value):
        if metadata is None:
            return ''
        
        res = ''
        for line in metadata.split('\n'):
            line = re.sub(r"\n$", "", line)
            if line.startswith(f"{field} "):
                line = re.sub(f"{field}[ ]+([^ ]*)", f"{field} {value}", line)
            res += line+"\n"
        return res

    def _set_content_field(self, content, field, value):
        if content is None:
            return ''
        
        res = ''
        for line in content.split('\n'):
            line = re.sub(r"\n$", "", line)
            if line.startswith(f"{field} "):
                line = re.sub(f"{field}[ ]+([^ ]*)[ ]+([^ ]*)", f"{field} {value} \\2", line)
            res += line+"\n"
        return res
        
        return ''

    def _format_content(self, symbol, content):
        if content is None or content=="":
            content = f"DEF {symbol.Name} U 0 40 Y Y 1 F N\n"
            content += 'F0 "U" -300 -500 50 H V C CNN\n'
            content += f'F1 "{symbol.Name}" -50 250 50 H V C CNN\n'
            content += 'F2 "" -150 0 50 H I C CNN\n'
            content += 'F3 "" -150 0 50 H I C CNN\n'
            content += "DRAW\n"
            content += "ENDDRAW\n"
            content += "ENDDEF\n"
        
        content = self._set_content_field(content, "DEF", symbol.Name)
        content = self._set_content_field(content, "F1", f'"{symbol.Name}'"")
        
        return content

    def _format_metadata(self, symbol, metadata):
        if metadata is None or metadata=="":
            metadata = f"$CMP {symbol.Name}\n"
            metadata += "$ENDCMP\n"
        
        metadata = self._set_metadata_field(metadata, "$CMP", symbol.Name)
        
        return metadata

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
            return self._get_metadata_field(self.symbol_model.metadata, "D")
        return self._get_metadata_field(self.symbol_file.Metadata, "D")
    
    @property
    def Metadata(self):
        if self.symbol_model is not None:
            return self.symbol_model.metadata
        return self.symbol_file.Metadata
        
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
            log.info(f"added symbol '{self.Name}' in file '{self._library.library_file.Path}' from database")
        elif self.symbol_file is not None and self.symbol_model is None:
            # symbol exists in file but not in database
            self.symbol_model = api.data.kicad_symbol.create()
            self.symbol_model.library = self._library.library_model
            self.symbol_model.name = self.symbol_file.Name
            self.symbol_model.content = self.symbol_file.Content
            self.symbol_model.metadata = self.symbol_file.Metadata
            self._library.library_model.symbols.add_pending(self.symbol_model)
            model_changed = True
            log.info(f"added symbol '{self.Name}' in database from file '{self._library.library_file.Path}'")
        elif self.symbol_file._content!=self.symbol_model.content or self.symbol_file._metadata!=self.symbol_model.metadata:
            delta = self._library.library_file.MtimeLib-self._library.library_model.mtime_lib

            if delta<=-DELTA_FILE:
                # database is newer than file
                self.symbol_file._content = self.symbol_model.content
                
                self.symbol_file._changed_lib = True
                file_changed = True
                log.info(f"updated symbol '{self.Name}' in file '{self._library.library_file.Path}' from database")
            elif delta>=DELTA_FILE:
                # file is newer than database
                self.symbol_model.content = self.symbol_file._content
                self._library.library_model.symbols.add_pending(self.symbol_model)
                model_changed = True
                log.info(f"updated symbol '{self.Name}' in database from file '{self._library.library_file.Path}'")

            delta = self._library.library_file.MtimeDcm-self._library.library_model.mtime_dcm

            if delta<=-DELTA_FILE:
                # database is newer than file
                self.symbol_file._metadata = self.symbol_model.metadata

                self.symbol_file._changed_dcm = True
                file_changed = True
                log.info(f"updated symbol '{self.Name}' in file '{self._library.library_file.DcmPath}' from database")
            elif delta>=DELTA_FILE:
                # file is newer than database
                self.symbol_model.metadata = self.symbol_file._metadata
                self._library.library_model.symbols.add_pending(self.symbol_model)
                model_changed = True
                log.info(f"updated symbol '{self.Name}' in database from file '{self._library.library_file.DcmPath}'")

        return (file_changed, model_changed)
    
    def _get_metadata_field(self, metadata, field):
        if metadata is None:
            return ''
        
        for line in metadata.split('\n'):
            line = re.sub(r"\n$", "", line)
            if line.startswith(f"{field} "):
                return re.sub(f"^{field} ", "", line)
        
        return ''

    def _get_content_field(self, content, field):
        if content is None:
            return ''
        
        for line in content.split('\n'):
            line = re.sub(r"\n$", "", line)
            if line.startswith(f"{field} "):
                return re.sub(f"^{field} ", "", line)
        
        return ''
    
    def __repr__(self):
        res = "<KicadSymbol> ("
        if self.symbol_file:
            res += f"file={self.symbol_file.Name} "
        if self.symbol_model:
            res += f"model={self.symbol_model.name}"
        res += ")"
        return res

class KicadSymbolLibrary():
    """
    This object is the bridge between library file and library record in database
    """
    
    def __init__(self, library_file=None, library_model=None):
        self.library_file = library_file
        self.library_model = library_model
        
        self._symbols = []
    
        if library_file is None and library_model is None:
            raise KicadSymbolLibraryException("Missing a file or a model for library")
        
        self._load_symbols()
        
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
            self.library_file = KicadSymbolLibraryFile(path=self.library_model.path)            
            self.library_file.Save(self.library_model.mtime_lib, self.library_model.mtime_dcm)
            log.info(f"created file '{self.library_file.path}'")
            
        elif self.library_file is not None and self.library_model is None:
            # library exists on disk but not in database
            self.library_model = api.data.kicad_symbol_library.create()
            self.library_model.path = self.library_file.Path
            self.library_model.mtime_lib = self.library_file.MtimeLib
            self.library_model.mtime_dcm = self.library_file.MtimeDcm
            api.data.kicad_symbol_library.save(self.library_model)
            log.info(f"created '{self.library_file.path}' in database")
    
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
            log.info(f"updated file '{self.library_file.path}'")

        if model_changed:
            self.library_model.mtime_lib = self.library_file.MtimeLib
            self.library_model.mtime_dcm = self.library_file.MtimeDcm
            api.data.kicad_symbol_library.save(self.library_model)
            log.info(f"updated '{self.library_model.path}' in database")
            
        log.debug(f"'{self.Path}' symbols: {self._symbols}")

    def __repr__(self):
        res = "<KicadSymbolLibrary> ("
        if self.library_file:
            res += f"file={self.library_file.Path} "
        if self.library_model:
            res += f"model={self.library_model.path}"
        res += ")"
        return res
    
class KicadSymbolLibraryManager(KicadFileManager):
    libraries = []
    folders = []
    loaded = False
    
    def __init__(self, owner):
        super(KicadSymbolLibraryManager, self).__init__(owner=owner, path=configuration.kicad_symbols_path) #, extensions=["lib", "dcm"])
        self._load()

    def Reload(self):
        KicadSymbolLibraryManager.loaded = False
        self._load()
    
    def Load(self):
        self._load()
        
    def _load(self):
        if KicadSymbolLibraryManager.loaded==False:
            self._load_file_libraries()
            self._load_model_libraries()
            for library in KicadSymbolLibraryManager.libraries:
                library._synchronize()
                
        KicadSymbolLibraryManager.loaded = True
        
    def _load_file_libraries(self):
        """
        Recurse all folders to find lib files
        """
        log.debug(f"KicadSymbolLibraryManager._load_file_libraries")
        
        libraries = KicadSymbolLibraryManager.libraries
        folders = KicadSymbolLibraryManager.folders
        
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
                libraries.append(KicadSymbolLibrary(library_file=KicadSymbolLibraryFile(rel_folder)))
        folders.remove('')
    
    def _load_model_libraries(self):
        log.debug(f"KicadSymbolLibraryManager._load_model_libraries")

        libraries = KicadSymbolLibraryManager.libraries
        folders = KicadSymbolLibraryManager.folders
        
        for library in api.data.kicad_symbol_library.find():
            libraryset = self._find_library(library.path)
            if libraryset is None:
                libraryset = KicadSymbolLibrary(library_model=library)
                libraries.append(libraryset)
            else:
                libraryset.library_model = library
                libraryset._load_symbols()
    
            # add folders
            pathel = self._cut_path(os.path.dirname(library.path))
            path = ''
            for el in pathel:
                path = os.path.join(path, el)
                if path not in folders:
                    folders.append(path)
    
        log.debug(f"folders: {self.folders}")
        log.debug(f"libraries: {self.libraries}")
        
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
        for library in KicadSymbolLibraryManager.libraries:
            if library.Path==path:
                return library
        return None
    
    def _add_folder(self, path):
        # TODO
        pass

    def _on_change_prehook(self, path):
#         if path.endswith(".lib") or path.endswith(".dcm") :
        KicadSymbolLibraryManager.loaded = False
        return True
        
    @property
    def Libraries(self):
        return KicadSymbolLibraryManager.libraries

    @property
    def Folders(self):
        return KicadSymbolLibraryManager.folders

    @staticmethod
    def CreateFolder(path):
        abspath = os.path.join(configuration.kicad_symbols_path, path)
        if os.path.exists(abspath):
            raise KicadFileManagerException(f"Folder '{path}' already exists")
        os.makedirs(abspath)
        
        KicadSymbolLibraryManager.loaded = False
        
    @staticmethod
    def MoveFolder(path, newpath):
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
        KicadSymbolLibraryManager.DisableNotificationsForPath(configuration.kicad_symbols_path, action=action)
        log.info(f"moved folder '{abspath}' to '{newabspath}'")
        
        # edit database
        for library in api.data.kicad_symbol_library.find():
            if library.path.startswith(path+os.sep):
                previous_path = library.path
                library.path = re.sub(f"^{path}", f"{newpath}", library.path)
                api.data.kicad_symbol_library.save(library)
                log.info(f"moved library '{previous_path}' to '{library.path}'")

        KicadSymbolLibraryManager.loaded = False

    @staticmethod
    def CreateLibrary(path):
        abspath = os.path.join(configuration.kicad_symbols_path, path)
        if os.path.exists(abspath):
            raise KicadFileManagerException(f"Library '{path}' already exists")
        
        library_file = KicadSymbolLibraryFile(path)
        KicadSymbolLibraryManager.DisableNotificationsForPath(configuration.kicad_symbols_path, action=library_file.Save)
        
        library = KicadSymbolLibrary(library_file)
        
        KicadSymbolLibraryManager.libraries.append(library)

        KicadSymbolLibraryManager.loaded = False

        return library

    @staticmethod
    def MoveLibrary(library, newpath):
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
        KicadSymbolLibraryManager.DisableNotificationsForPath(configuration.kicad_symbols_path, action=action)
        
        library.library_model.path = os.path.join(newpath, newname)
        api.data.kicad_symbol_library.save(library.library_model)
        
        log.info(f"library '{previousname}' renamed to '{os.path.join(newpath, newname)}'")

        KicadSymbolLibraryManager.loaded = False

        return library
    
    @staticmethod
    def RemoveLibrary(library):
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
            if library.library_file is not None and os.path.exists(library.library_file.AbsDcmPath):
                os.remove(library.library_file.AbsDcmPath)
        KicadSymbolLibraryManager.DisableNotificationsForPath(configuration.kicad_symbols_path, action=action)

        KicadSymbolLibraryManager.loaded = False

        log.info(f"library '{library.Path}' removed")

    @staticmethod
    def RemoveFolder(path):
#         if len(os.listdir(os.path.join(configuration.kicad_symbols_path, path)))>0:
#             raise KicadFileManagerException(f"Folder '{path}' is not empty")
        def action():
            shutil.rmtree(os.path.join(configuration.kicad_symbols_path, path))
        KicadSymbolLibraryManager.DisableNotificationsForPath(configuration.kicad_symbols_path, action=action)

        KicadSymbolLibraryManager.loaded = False

        log.info(f"folder '{path}' removed")

    @staticmethod
    def CreateSymbol(library, name, content="", metadata=""):
        for s in library.Symbols:
            if name==s.Name:
                raise KicadFileManagerException(f"Symbol '{name}' already exists in library '{library.Path}'")
            
        symbol = KicadSymbol(library)
        
        if library.library_file is not None:
            symbol.symbol_file = KicadSymbolFile(library.library_file, name=name, content=content, metadata=metadata)
            library.library_file._symbols.append(symbol.symbol_file)
            library.library_file._changed_lib = True
            library.library_file._changed_dcm = True
            library.library_file.Save()
        
        if library.library_model is not None:
            symbol.symbol_model = api.data.kicad_symbol.create()
            symbol.symbol_model.library = library.library_model
            symbol.symbol_model.name = name
            symbol.symbol_model.content = content
            symbol.symbol_model.metadata = metadata
            library.library_model.symbols.add_pending(symbol.symbol_model)
            if library.library_file is not None:
                library.library_model.mtime_lib = library.library_file.MtimeLib
                library.library_model.mtime_dcm = library.library_file.MtimeDcm
            library.library_model.save()
            
        library._symbols.append(symbol)
        
        KicadSymbolLibraryManager.loaded = False
        
        return symbol
    
    @staticmethod
    def RenameSymbol(symbol, newname):
        for s in symbol.Library.Symbols:
            if newname==s.Name:
                raise KicadFileManagerException(f"Symbol '{newname}' already exists in library '{symbol.Library.Path}'")

        if symbol.symbol_file is not None:
            symbol.symbol_file._name = newname
            
            symbol.symbol_file._changed_lib = True
            symbol.symbol_file._changed_dcm = True
            symbol.Library.library_file.Save()
            
        if symbol.symbol_model is not None:
            symbol.symbol_model.name = newname
            symbol.symbol_model.save()
            symbol.Library.library_model.mtime_lib = symbol.Library.library_file.MtimeLib
            symbol.Library.library_model.mtime_dcm = symbol.Library.library_file.MtimeDcm
            symbol.Library.library_model.save()

        KicadSymbolLibraryManager.loaded = False

    @staticmethod
    def RemoveSymbol(symbol):
        library = symbol.Library

        associated_parts = api.data.part.find([api.data.part.FilterSymbols([symbol.symbol_model])])
        for associated_part in associated_parts:
            log.info(f"part '{associated_part.name} dissociated from {associated_part.symbol.name}")
            associated_part.symbol = None
            associated_part.save()

        if symbol.symbol_file is not None:
            library.library_file._symbols.remove(symbol.symbol_file)
            library.library_file._changed_lib = True
            library.library_file.Save()
            
        if symbol.symbol_model is not None:
            symbol.symbol_model.delete()
            library.library_model.mtime_lib = library.library_file.MtimeLib
            library.library_model.mtime_dcm = library.library_file.MtimeDcm
            library.library_model.save()
            
        library._symbols.remove(symbol)

        KicadSymbolLibraryManager.loaded = False
