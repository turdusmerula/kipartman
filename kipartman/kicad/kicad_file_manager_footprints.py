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

class KicadFootprintLibraryException(Exception):
    def __init__(self, error):
        super(KicadFootprintLibraryException, self).__init__(error)

class KicadFootprintFile():
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
    
    @Name.setter
    def Name(self):
        self._name
        self._changed_lib = True
        self._changed_dcm = True
        
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
class KicadFootprintLibraryFile(File):
    def __init__(self, path):
        super(KicadFootprintLibraryFile, self).__init__(path)
        self._footprints = []
        
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
        return os.path.join(configuration.kicad_footprints_path, self.Path)
    
    @property
    def AbsDcmPath(self):
        return re.sub(r"\.lib$", ".dcm", self.AbsPath)
        
    @property
    def DcmPath(self):
        return re.sub(r"\.lib$", ".dcm", self.Path)

    @property
    def Footprints(self):
#         self._read_lib_file()
#         self._read_metadata_file()
#         if self._loaded_lib==False:
#         if self._loaded_dcm==False:
        return self._footprints

    @property
    def ChangedLib(self):
        res = self._changed_lib
        if res==False:
            for footprint in self._footprints:
                if footprint.ChangedLib:
                    return True
            return False
        return True
    
    @property
    def ChangedDcm(self):
        res = self._changed_dcm
        if res==False:
            for footprint in self._footprints:
                if footprint.ChangedDcm:
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

    def HasFootprint(self, name):
        for footprint in self.Footprints:
            if footprint.Name==name:
                return True
        return False
    
    def AddFootprint(self, footprint):
        if self.HasFootprint(footprint.Name):
            raise KicadFootprintLibraryException(f"Footprint {footprint.Name} already exists in {self.Path}")
        self._footprints.append(footprint)
        footprint._library = self
        self._changed = True
        
    def RemoveFootprint(self, footprint):
        if self.HasFootprint(footprint.name)==False:
            raise KicadFootprintLibraryException(f"Footprint {footprint.name} does not exists in {self.Path}")
        for s in self._footprints:
            if s.Name==footprint.Name:
                self._footprints.remove(s)
                break
        self._changed = True

    def _read_lib_file(self):
        self._footprints = []
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
                for footprint in self._footprints:
                    if footprint.Name==name+dup:
                        dup = f"_{dupn}"
                        dupn += 1
                if dup!="":
                    log.info(f"duplication found in '{self.Path}', renamed to '{name+dup}'")
                    
                self._footprints.append(KicadFootprintFile(self, name+dup, content))
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
                for footprint in self._footprints:
                    if footprint.Name==name:
                        footprint._metadata = metadata
                metadata = ''
            else:
                metadata += line+'\n'
    
        self._loaded_dcm = True

    def _save_lib_file(self, mtime=None):
        log.debug(f"KicadFootprintLibraryFile._save_lib_file {self.AbsPath}")

        os.makedirs(os.path.dirname(self.AbsPath), exist_ok=True)
        with open(self.AbsPath, 'w', encoding='utf-8') as file:
            # TODO add generated from kicad
            file.write('EESchema-LIBRARY Version 2.3\n')
            file.write('#encoding utf-8\n')
 
            for footprint in self._footprints:
                file.write("#\n")
                file.write(f"# {footprint.Name}\n")
                file.write("#\n")
                file.write(footprint.Content)
             
            file.write('#\n')
            file.write('#End Library\n')

        if mtime is not None:
            # set last modification date to updated
            os.utime(self.AbsPath, (mtime, mtime))

    def _save_metadata_file(self, mtime=None):
        log.debug(f"KicadFootprintLibraryFile._save_metadata_file {self.AbsDcmPath}")
        os.makedirs(os.path.dirname(self.AbsDcmPath), exist_ok=True)
        with open(self.AbsDcmPath, 'w', encoding='utf-8') as file:
            # TODO add generated from kicad
            file.write('EESchema-DOCLIB  Version 2.0\n')
 
            for footprint in self._footprints:
                if footprint.Metadata!="":
                    file.write("#\n")
                    file.write(footprint.Metadata)
                 
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
                for footprint in self._footprints:
                    footprint._changed_lib = False
                
            if self.ChangedDcm:
                self._save_metadata_file(mtimedcm)
                self._changed_dcm = False
                self._loaded_dcm = True
                for footprint in self._footprints:
                    footprint._changed_dcm = False
                
                
        KicadFileManager.DisableNotificationsForPath(self.AbsPath, action)

    def SaveLib(self, mtimelib=None):
        def action():
            self._save_lib_file(mtimelib)
        KicadFileManager.DisableNotificationsForPath(self.AbsPath, action)

    def SaveDcm(self, mtimedcm=None):
        def action():
            self._save_metadata_file(mtimedcm)
        KicadFileManager.DisableNotificationsForPath(self.AbsPath, action)

class KicadFootprint():
    """
    This object is the bridge between footprint in library file and footprint record in database
    """
    
    def __init__(self, library, footprint_file=None, footprint_model=None):
        self.footprint_file = footprint_file
        self.footprint_model = footprint_model
        self._library = library
    
    @property
    def Library(self):
        return self._library
     
    @property
    def Name(self):
        if self.footprint_model is not None:
            return self.footprint_model.name
        return self.footprint_file.Name
    
    @property
    def Content(self):
        if self.footprint_model is not None:
            return self.footprint_model.content
        return self.footprint_file.Content

    @property
    def Description(self):
        if self.footprint_model is not None:
            return self._get_metadata(self.footprint_model.metadata, "D")
        return self._get_metadata(self.footprint_file.Metadata, "D")
    
    
    def _synchronize(self):
        file_changed = False
        model_changed = False
        
        if self.footprint_file is None and self.footprint_model is not None:
            # footprint exists in database but not in file
            self._footprint_file = KicadFootprintFile(self._library.library_file, self.footprint_model.name, self.footprint_model.content, self.footprint_model.metadata)
            self._footprint_file._changed_lib = True
            self._footprint_file._changed_dcm = True
            self._library.library_file.AddFootprint(self._footprint_file)
            file_changed = True
            log.info(f"added footprint '{self.Name}' in file '{self._library.library_file.Path}' from database")
        elif self.footprint_file is not None and self.footprint_model is None:
            # footprint exists in file but not in database
            self.footprint_model = api.data.library_footprint.create()
            self.footprint_model.library = self._library.library_model
            self.footprint_model.name = self.footprint_file.Name
            self.footprint_model.content = self.footprint_file.Content
            self.footprint_model.metadata = self.footprint_file.Metadata
            self._library.library_model.footprints.add_pending(self.footprint_model)
            model_changed = True
            log.info(f"added footprint '{self.Name}' in database from file '{self._library.library_file.Path}'")
        elif self.footprint_file._content!=self.footprint_model.content or self.footprint_file._metadata!=self.footprint_model.metadata:
            delta = self._library.library_file.MtimeLib-self._library.library_model.mtime_lib

            if delta<=-DELTA_FILE:
                # database is newer than file
                self.footprint_file._content = self.footprint_model.content
                self.footprint_file._changed_lib = True
                file_changed = True
                log.info(f"updated footprint '{self.Name}' in file '{self._library.library_file.Path}' from database")
            elif delta>=DELTA_FILE:
                # file is newer than database
                self.footprint_model.content = self.footprint_file._content
                self._library.library_model.footprints.add_pending(self.footprint_model)
                model_changed = True
                log.info(f"updated footprint '{self.Name}' in database from file '{self._library.library_file.Path}'")

            delta = self._library.library_file.MtimeDcm-self._library.library_model.mtime_dcm

            if delta<=-DELTA_FILE:
                # database is newer than file
                self.footprint_file._metadata = self.footprint_model.metadata
                self.footprint_file._changed_dcm = True
                file_changed = True
                log.info(f"updated footprint '{self.Name}' in file '{self._library.library_file.DcmPath}' from database")
            elif delta>=DELTA_FILE:
                # file is newer than database
                self.footprint_model.metadata = self.footprint_file._metadata
                self._library.library_model.footprints.add_pending(self.footprint_model)
                model_changed = True
                log.info(f"updated footprint '{self.Name}' in database from file '{self._library.library_file.DcmPath}'")

        return (file_changed, model_changed)
    
    def _get_metadata(self, metadata, field):
        if metadata is None:
            return ''
        
        for line in metadata.split('\n'):
            line = re.sub(r"\n$", "", line)
            if line.startswith(f"{field} "):
                return re.sub(f"^{field} ", "", line)
        
        return ''

    def __repr__(self):
        res = "<KicadFootprint> ("
        if self.footprint_file:
            res += f"file={self.footprint_file.Name} "
        if self.footprint_model:
            res += f"model={self.footprint_model.name}"
        res += ")"
        return res

class KicadFootprintLibrary():
    """
    This object is the bridge between library file and library record in database
    """
    
    def __init__(self, library_file=None, library_model=None):
        self.library_file = library_file
        self.library_model = library_model
        
        self._footprints = []
    
        if library_file is None and library_model is None:
            raise KicadFootprintLibraryException("Missing a file or a model for library")
        
        self._load_footprints()
        
    @property
    def AbsPath(self):
        if self.library_model is not None:
            return os.path.join(configuration.kicad_footprints_path, self.library_model.path)
        return self.library_file.AbsPath
    
    @property
    def Path(self):
        if self.library_model is not None:
            return self.library_model.path
        return self.library_file.Path

    @property
    def Footprints(self):
        return self._footprints
    
    def _load_footprints(self):
        self._footprints = []
        
        if self.library_file is not None:
            for footprint in self.library_file.Footprints:
                self._footprints.append(KicadFootprint(library=self, footprint_file=footprint))
        
        if self.library_model is not None:
            for footprint in self.library_model.footprints.all():
                footprintset = self._find_footprint(footprint.name)
                if footprintset is None:
                    footprintset = KicadFootprint(library=self, footprint_model=footprint)
                    self._footprints.append(footprintset)
                else:
                    footprintset.footprint_model = footprint

    def _find_footprint(self, name):
        for footprint in self._footprints:
            if footprint.Name==name:
                return footprint
    
    def _synchronize(self):
        """
        synchronize file and database
        """

        if self.library_file is None and self.library_model is not None:
            # library exists in database but not on disk
            # create it on disk
            self.library_file = KicadFootprintLibraryFile(path=self.library_model.path)            
            self.library_file.Save(self.library_model.mtime_lib, self.library_model.mtime_dcm)
            log.info(f"created file '{self.library_file.path}'")
            
        elif self.library_file is not None and self.library_model is None:
            # library exists on disk but not in database
            self.library_model = api.data.library.create()
            self.library_model.path = self.library_file.Path
            self.library_model.mtime_lib = self.library_file.MtimeLib
            self.library_model.mtime_dcm = self.library_file.MtimeDcm
            api.data.library.save(self.library_model)
            log.info(f"created '{self.library_file.path}' in database")
    
        # at this point both library_file and library_model are presents
        
        file_changed = False
        model_changed = False
        for footprint in self._footprints:
            fc, mc = footprint._synchronize()
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
            api.data.library.save(self.library_model)
            log.info(f"updated '{self.library_model.path}' in database")
            
        log.debug(f"'{self.Path}' footprints: {self._footprints}")

    def __repr__(self):
        res = "<KicadFootprintLibrary> ("
        if self.library_file:
            res += f"file={self.library_file.Path} "
        if self.library_model:
            res += f"model={self.library_model.path}"
        res += ")"
        return res
    
class KicadFootprintLibraryManager(KicadFileManager):
    libraries = []
    folders = []
    loaded = False
    
    def __init__(self, owner):
        super(KicadFootprintLibraryManager, self).__init__(owner=owner, path=configuration.kicad_footprints_path) #, extensions=["lib", "dcm"])
        self._load()

    def Reload(self):
        KicadFootprintLibraryManager.loaded = False
        self._load()
    
    def Load(self):
        self._load()
        
    def _load(self):
        pass
#         if KicadFootprintLibraryManager.loaded==False:
#             self._load_file_libraries()
#             self._load_model_libraries()
#             for library in KicadFootprintLibraryManager.libraries:
#                 library._synchronize()
#                 
#         KicadFootprintLibraryManager.loaded = True
        
    def _load_file_libraries(self):
        """
        Recurse all folders to find lib files
        """
        log.debug(f"KicadFootprintLibraryManager._load_file_libraries")
        
        libraries = KicadFootprintLibraryManager.libraries
        folders = KicadFootprintLibraryManager.folders
        
        libraries.clear()
        folders.clear()
        
        basepath = os.path.normpath(os.path.abspath(configuration.kicad_footprints_path))
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
                libraries.append(KicadFootprintLibrary(library_file=KicadFootprintLibraryFile(rel_folder)))
        folders.remove('')
    
    def _load_model_libraries(self):
        log.debug(f"KicadFootprintLibraryManager._load_model_libraries")

        libraries = KicadFootprintLibraryManager.libraries
        folders = KicadFootprintLibraryManager.folders
        
        for library in api.data.library.find():
            libraryset = self._find_library(library.path)
            if libraryset is None:
                libraryset = KicadFootprintLibrary(library_model=library)
                libraries.append(libraryset)
            else:
                libraryset.library_model = library
                libraryset._load_footprints()
    
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
        for library in KicadFootprintLibraryManager.libraries:
            if library.Path==path:
                return library
        return None
    
    def _add_folder(self, path):
        # TODO
        pass

    def _on_change_prehook(self, path):
#         if path.endswith(".lib") or path.endswith(".dcm") :
        KicadFootprintLibraryManager.loaded = False
        return True
        
    @property
    def Libraries(self):
        return KicadFootprintLibraryManager.libraries

    @property
    def Folders(self):
        return KicadFootprintLibraryManager.folders

    def CreateFolder(self, path):
        abspath = os.path.join(configuration.kicad_footprints_path, path)
        if os.path.exists(abspath):
            raise KicadFileManagerException(f"Folder '{path}' already exists")
        os.makedirs(abspath)
        
    def MoveFolder(self, path, newpath):
        abspath = os.path.join(configuration.kicad_footprints_path, path)
        if os.path.exists(abspath)==False:
            raise KicadFileManagerException(f"Folder '{path}' does not exists")
        newabspath = os.path.join(configuration.kicad_footprints_path, newpath)
        if os.path.exists(newabspath):
            raise KicadFileManagerException(f"Folder '{newpath}' already exists")
        
        # move files
        def action():
            os.makedirs(os.path.dirname(abspath), exist_ok=True)
            os.rename(abspath, newabspath)
        self.DisableNotificationsForPath(configuration.kicad_footprints_path, action=action)
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
        abspath = os.path.join(configuration.kicad_footprints_path, path)
        if os.path.exists(abspath):
            raise KicadFileManagerException(f"Library '{path}' already exists")
        
        library_file = KicadFootprintLibraryFile(path)
        self.DisableNotificationsForPath(configuration.kicad_footprints_path, action=library_file.Save)
        
        library = KicadFootprintLibrary(library_file)
        
        KicadFootprintLibraryManager.libraries.append(library)

        return library

    def MoveLibrary(self, library, newpath):
        previousname = library.Path
        newname = os.path.basename(newpath)
        newpath = os.path.dirname(newpath)
        newabspath = os.path.join(configuration.kicad_footprints_path, newpath)
        
        if os.path.exists(newabspath)==False:
            raise KicadFileManagerException(f"Folder '{newpath}' does not exists")
        if newname.endswith(".lib")==False:
            raise KicadFileManagerException(f"'{newname}' is not a valid library name")
        
        def action():
            os.rename(library.AbsPath, os.path.join(newabspath, newname))
        self.DisableNotificationsForPath(configuration.kicad_footprints_path, action=action)
        
        library.library_model.path = os.path.join(newpath, newname)
        api.data.library.save(library.library_model)
        
        log.info(f"library '{previousname}' renamed to '{os.path.join(newpath, newname)}'")

        return library
    
    def DeleteLibrary(self, library):
        footprints_to_remove = []
        for footprint in library.Footprints:
            footprints_to_remove.append(footprint.footprint_model)
        
        associated_parts = api.data.part.find([api.data.part.FilterFootprints(footprints_to_remove)])
        for associated_part in associated_parts:
            log.info(f"part '{associated_part.name} dissociated from {associated_part.footprint.name}")
            associated_part.footprint = None
            associated_part.save()
        
        library.library_model.delete()
        def action():
            os.remove(library.AbsPath)
        self.DisableNotificationsForPath(configuration.kicad_footprints_path, action=action)

        log.info(f"library '{library.Path}' removed")

    def DeleteFolder(self, path):
#         if len(os.listdir(os.path.join(configuration.kicad_footprints_path, path)))>0:
#             raise KicadFileManagerException(f"Folder '{path}' is not empty")
        def action():
            shutil.rmtree(os.path.join(configuration.kicad_footprints_path, path))
        self.DisableNotificationsForPath(configuration.kicad_footprints_path, action=action)

        log.info(f"folder '{path}' removed")
        


# class KicadFileManagerPretty(KicadFileManager):
#     def __init__(self):
#         super(KicadFileManagerPretty, self).__init__()
# 
#         self.extensions = ['kicad_mod']
#         
#     def root_path(self):
#         return configuration.kicad_footprints_path
# 
#     def version_file(self):
#         return '.kiversion_mod'
# 
#     def category(self):
#         return 'pretty'
#     
#     def Load(self):
#         """
#         fill cache files from disk
#         """
#         self.files = {}
#         libraries, self.folders = self.GetLibraries()
#         
#         for library in libraries:
#             footprints = self.GetFootprints(library)
#             for footprint in footprints:
#                 source_path = os.path.join(library, footprint)
#                 content = Path(os.path.join(self.root_path(), source_path)).read_text()
#                 md5 = hash.md5(content).hexdigest()
#  
#                 file = File()
#                 file.source_path = source_path
#                 file.md5 = md5
# 
#                 self.files[source_path] = file
# 
# 
#     def GetLibraries(self, root_path=None):
#         """
#         Recurse all folders and return .pretty folders path
#         @param root_path: path from which to start recursing, None starts from root
#         """
#         log.debug("===> GetLibraries----")
#         basepath = os.path.normpath(os.path.abspath(self.root_path()))
#         to_explore = [basepath]
#         libraries = []
#         folders = []
#         
#         while len(to_explore)>0:
#             path = to_explore.pop()
#             if os.path.exists(path):
#                 for folder in glob(os.path.join(path, "*/")):
#                     if folder!='/':
#                         folders.append(os.path.relpath(os.path.normpath(os.path.abspath(folder)), basepath))
#                         if re.compile("^.*\.pretty$").match(os.path.normpath(os.path.abspath(folder))):
#                             #print("=>", folder) 
#                             libraries.append(os.path.relpath(os.path.normpath(os.path.abspath(folder)), basepath))
#                         elif os.path.normpath(os.path.abspath(folder))!=os.path.normpath(os.path.abspath(path)):
#                             to_explore.append(folder)
#         #print("---------------------")
#      
#         return libraries, folders
# 
#     def GetFootprints(self, library_path):
#         """
#         Return all footprints in a pretty lib
#         """
#         #log.debug("===> GetFootprints----")
#         footprints = []
#  
#         path = os.path.join(self.root_path(), library_path)        
#         if os.path.exists(path):
#             for kicad_mod in glob(os.path.join(path, "*.kicad_mod")):
#                 #print("==>", kicad_mod) 
#                 footprints.append(os.path.basename(kicad_mod))
#         #print("----------------------")
#      
#         return footprints
#  
#     def Exists(self, path):
#         return os.path.exists(os.path.join(self.root_path(), path))
# 
#     def CreateFile(self, path, content, overwrite=False):
#         if self.Exists(path) and overwrite==False:
#             raise KicadFileManagerException('File %s already exists'%path)
# 
#         fullpath = os.path.join(self.root_path(), path)
#         if not os.path.exists(os.path.dirname(fullpath)):
#             os.makedirs(os.path.dirname(fullpath))
#         
#         with open(fullpath, 'w', encoding='utf-8') as content_file:
#             if content:
#                 content_file.write(content)
#             else:
#                 content_file.write('')
#         content_file.close() 
# 
#         file = File()
#         file.source_path = path
#         file.md5 = hash.md5(content).hexdigest()
#         file.updated = rest.api.get_date()
#         file.category = self.category()
# 
#         return file
#     
#     def EditFile(self, file, content, create=False):
#         if self.Exists(file.source_path)==False and create==False:
#             raise KicadFileManagerException('File %s does not exists'%file.source_path)
# 
#         fullpath = os.path.join(self.root_path(), file.source_path)
#         if self.Exists(file.source_path)==True:
#             md5file = hash.md5(Path(fullpath).read_text()).hexdigest()
#             md5 = hash.md5(content).hexdigest()
#             if md5==md5file:
#                 return file, False
#         
#         if os.path.exists(os.path.dirname(fullpath))==False:
#             os.makedirs(os.path.dirname(fullpath))
#         with open(fullpath, 'w', encoding='utf-8') as content_file:
#             if content:
#                 content_file.write(content)
#             else:
#                 content_file.write('')
#         content_file.close() 
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
#         os.rename(os.path.join(self.root_path(), file.source_path), 
#                          os.path.join(self.root_path(), dest_path))
# 
#         file.source_path = dest_path
#         #fullpath = os.path.join(self.root_path(), file.source_path)
#         #file.updated = datetime.datetime.fromtimestamp(os.path.getmtime(fullpath)).strftime("%Y-%m-%dT%H:%M:%SZ")
#         file.updated = rest.api.get_date()
#         
#         return file
# 
#     def DeleteFile(self, file, force=False):
#         if self.Exists(file.source_path)==False and force==False:
#             raise KicadFileManagerException('File %s does not exists'%file.source_path)
#         
#         fullpath = os.path.join(self.root_path(), file.source_path)
#         if os.path.exists(fullpath):
#             os.remove(fullpath)
#         #file.updated = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
#         file.updated = rest.api.get_date()
#     
#         return file
#     
#     def LoadContent(self, file):
#         if self.Exists(file.source_path)==False:
#             raise KicadFileManagerException('File %s does not exists'%file.source_path)
#         
#         fullpath = os.path.join(self.root_path(), file.source_path)
#         with open(fullpath, encoding='utf-8') as f:
#             file.content = f.read()
# 
#     def CreateFolder(self, path):
#         abspath = os.path.join(self.root_path(), path)
#         if os.path.exists(abspath):
#             raise KicadFileManagerException('Folder %s already exists'%path)
#         else:
#             os.makedirs(abspath)
#     
#     def MoveFolder(self, source_path, dest_path):
#         abs_source_path = os.path.join(self.root_path(), source_path)
#         abs_dest_path = os.path.join(self.root_path(), dest_path)
#         if os.path.exists(abs_source_path)==False:
#             raise KicadFileManagerException('Folder %s does not exists'%abs_source_path)
#         if os.path.exists(abs_dest_path):
#             raise KicadFileManagerException('Folder %s already exists'%abs_dest_path)
#         shutil.move(abs_source_path, abs_dest_path)
#     
#     def DeleteFolder(self, path):
#         abspath = os.path.join(self.root_path(), path)
#         shutil.rmtree(abspath)
#      
# 
# def replace_last(source_string, replace_what, replace_with):
#     head, _sep, tail = source_string.rpartition(replace_what)
#     return head + replace_with + tail
