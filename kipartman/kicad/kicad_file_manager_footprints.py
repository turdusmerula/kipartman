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
    def __init__(self, library, name, content):
        self._library = library
        self._name = name
        self._content = content

    @property
    def Library(self):
        return self._library
    
    @property
    def Path(self):
        return os.path.join(self._library.Path, self._name+".kicad_mod")
    
    @property
    def AbsPath(self):
        return os.path.join(configuration.kicad_footprints_path, self.Path)

    @property
    def Name(self):
        return self._name
        
    @property
    def Mtime(self):
        return os.path.getmtime(self.AbsPath)
        
    @property
    def Content(self):
        return self._content

    def _save_footprint_file(self, mtime=None):
        log.debug(f"KicadFootprintFile._save_footprint_file {self.AbsPath}")

        os.makedirs(os.path.dirname(self.AbsPath), exist_ok=True)
        with open(self.AbsPath, 'w', encoding='utf-8') as file:
            file.write(self._content)

        if mtime is not None:
            # set last modification date to updated
            os.utime(self.AbsPath, (mtime, mtime))

    def Save(self, mtime=None):
        def action():
            self._save_footprint_file(mtime)
            self._changed = False
            self._loaded = True
                 
        KicadFileManager.DisableNotificationsForPath(self.AbsPath, action)

    def __repr__(self):
        res = f"<KicadFootprintFile> ({self.Name})"
        return res

#     def _
class KicadFootprintLibraryFile(File):
    def __init__(self, path):
        super(KicadFootprintLibraryFile, self).__init__(path)
        self._footprints = []
        
        if os.path.exists(self.AbsPath)==False:
            self._loaded = True
        else:
            self._loaded = False
    
        self._read_lib_folder()
    
    @property
    def AbsPath(self):
        return os.path.join(configuration.kicad_footprints_path, self.Path)
    
    @property
    def Footprints(self):
        return self._footprints
    
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

    def _read_lib_folder(self):
        self._footprints = []
        if(os.path.isdir(self.AbsPath)==False):
            return

        for path in glob(os.path.join(self.AbsPath, '*')):
            if os.path.isfile(path) and path.endswith(".kicad_mod"):
                with open(path, "r", encoding='utf-8') as f:
                    content = f.read()
                name = re.sub(r".*/(.*)\.kicad_mod$", r"\1", path)
                self._footprints.append(KicadFootprintFile(self, name, content))

        self._loaded = True
        
    def Save(self):
        def action():
            os.makedirs(self.AbsPath, exist_ok=True)
                 
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
    def Path(self):
        if self.footprint_model is not None:
            return os.path.join(self.footprint_model.library.path, self.footprint_model.name+".kicad_mod")
        return self.footprint_file.Path
    
    @property
    def Content(self):
        if self.footprint_model is not None:
            return self.footprint_model.content
        return self.footprint_file.Content
    
    def _synchronize(self):
        if self.footprint_file is None and self.footprint_model is not None:
            # footprint exists in database but not in file
            self._footprint_file = KicadFootprintFile(self._library.library_folder, self.footprint_model.name, self.footprint_model.content)
            self._footprint_file._changed = True
            # TODO mtime
            self._library.library_folder.AddFootprint(self._footprint_file)
            self._footprint_file.Save(mtime=self.footprint_model.mtime)
            log.info(f"added footprint file '{self.Path}' in library folder '{self._library.library_folder.Path}' from database")
        elif self.footprint_file is not None and self.footprint_model is None:
            # footprint exists in file but not in database
            self.footprint_model = api.data.kicad_footprint.create()
            self.footprint_model.library = self._library.library_model
            self.footprint_model.name = self.footprint_file.Name
            self.footprint_model.content = self.footprint_file.Content
            self.footprint_model.mtime = self.footprint_file.Mtime
            api.data.kicad_footprint.save(self.footprint_model)
            log.info(f"added footprint '{self.Name}' in database from library folder '{self._library.library_folder.Path}'")
        elif self.footprint_file._content!=self.footprint_model.content:
            delta = self.footprint_file.Mtime-self.footprint_model.mtime
 
            if delta<=-DELTA_FILE:
                # database is newer than file
                self.footprint_file._content = self.footprint_model.content
                self.footprint_file.Save(mtime=self.footprint_model.mtime)
                log.info(f"updated footprint '{self.Name}' in library folder '{self._library.library_folder.Path}' from database")
            elif delta>=DELTA_FILE:
                # file is newer than database
                self.footprint_model.content = self.footprint_file.Content
                self.footprint_model.mtime = self.footprint_file.Mtime
                api.data.kicad_footprint.save(self.footprint_model)
                log.info(f"updated footprint '{self.Name}' in database from library folder '{self._library.library_folder.Path}'")

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
    This object is the bridge between library on disk and library record in database
    """
    
    def __init__(self, library_folder=None, library_model=None):
        self.library_folder = library_folder
        self.library_model = library_model
        
        self._footprints = []
    
        if library_folder is None and library_model is None:
            raise KicadFootprintLibraryException("Missing a file or a model for library")
        
        self._load_footprints()
        
    @property
    def AbsPath(self):
        if self.library_model is not None:
            return os.path.join(configuration.kicad_footprints_path, self.library_model.path)
        return self.library_folder.AbsPath
    
    @property
    def Path(self):
        if self.library_model is not None:
            return self.library_model.path
        return self.library_folder.Path

    @property
    def Footprints(self):
        return self._footprints
    
    def _load_footprints(self):
        self._footprints = []
        
        if self.library_folder is not None:
            for footprint in self.library_folder.Footprints:
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

        if self.library_folder is None and self.library_model is not None:
            # library exists in database but not on disk
            # create it on disk
            self.library_folder = KicadFootprintLibraryFile(path=self.library_model.path)            
            self.library_folder.Save()
            log.info(f"created library folder '{self.library_folder.path}'")
             
        elif self.library_folder is not None and self.library_model is None:
            # library exists on disk but not in database
            self.library_model = api.data.kicad_footprint_library.create()
            self.library_model.path = self.library_folder.Path
            api.data.kicad_footprint_library.save(self.library_model)
            log.info(f"created library '{self.library_folder.path}' in database")
     
        # at this point both library_folder and library_model are presents
         
        for footprint in self._footprints:
            footprint._synchronize()
            
        log.debug(f"'{self.Path}' footprints: {self._footprints}")

    def __repr__(self):
        res = "<KicadFootprintLibrary> ("
        if self.library_folder:
            res += f"file={self.library_folder.Path} "
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
        if KicadFootprintLibraryManager.loaded==False:
            self._load_file_libraries()
            self._load_model_libraries()
            for library in KicadFootprintLibraryManager.libraries:
                library._synchronize()
                 
        KicadFootprintLibraryManager.loaded = True
        
    def _load_file_libraries(self):
        """
        Recurse all folders to find libraries
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
                    if folder!='/' and folder.endswith(".pretty/")==False:
                        folders.append(os.path.relpath(os.path.normpath(os.path.abspath(folder)), basepath))
                        if os.path.normpath(os.path.abspath(folder))!=os.path.normpath(os.path.abspath(path)):
                            to_explore.append(folder)
        
        folders.append('')
        # search for libs in folders
        for folder in folders:
            for lib in glob(os.path.join(basepath, folder, "*.pretty")):
                rel_folder = os.path.relpath(os.path.normpath(os.path.abspath(lib)), basepath)
                libraries.append(KicadFootprintLibrary(library_folder=KicadFootprintLibraryFile(rel_folder)))
        folders.remove('')
    
    def _load_model_libraries(self):
        log.debug(f"KicadFootprintLibraryManager._load_model_libraries")
 
        libraries = KicadFootprintLibraryManager.libraries
        folders = KicadFootprintLibraryManager.folders
         
        for library in api.data.kicad_footprint_library.find():
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
        for library in api.data.kicad_footprint_library.find():
            if library.path.startswith(path+os.sep):
                previous_path = library.path
                library.path = re.sub(f"^{path}", f"{newpath}", library.path)
                api.data.kicad_footprint_library.save(library)
                log.info(f"moved library '{previous_path}' to '{library.path}'")
         
    def CreateLibrary(self, path):
        abspath = os.path.join(configuration.kicad_footprints_path, path)
        if os.path.exists(abspath):
            raise KicadFileManagerException(f"Library '{path}' already exists")
         
        library_folder = KicadFootprintLibraryFile(path)
        library_folder.Save()
         
        library = KicadFootprintLibrary(library_folder)
         
        KicadFootprintLibraryManager.libraries.append(library)
 
        return library
 
    def MoveLibrary(self, library, newpath):
        previousname = library.Path
        newname = os.path.basename(newpath)
        newpath = os.path.dirname(newpath)
        newabspath = os.path.join(configuration.kicad_footprints_path, newpath)
          
        if os.path.exists(newabspath)==False:
            raise KicadFileManagerException(f"Folder '{newpath}' does not exists")
        if newname.endswith(".pretty")==False:
            raise KicadFileManagerException(f"'{newname}' is not a valid library name")
          
        def action():
            os.rename(library.AbsPath, os.path.join(newabspath, newname))
        self.DisableNotificationsForPath(configuration.kicad_footprints_path, action=action)
          
        library.library_model.path = os.path.join(newpath, newname)
        api.data.kicad_footprint_library.save(library.library_model)
          
        log.info(f"library '{previousname}' renamed to '{os.path.join(newpath, newname)}'")
 
        return library
     
    def RemoveLibrary(self, library):
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
            shutil.rmtree(library.AbsPath)
        self.DisableNotificationsForPath(configuration.kicad_footprints_path, action=action)
 
        log.info(f"library '{library.Path}' removed")
 
    def DeleteFolder(self, path):
#         if len(os.listdir(os.path.join(configuration.kicad_footprints_path, path)))>0:
#             raise KicadFileManagerException(f"Folder '{path}' is not empty")
        def action():
            shutil.rmtree(os.path.join(configuration.kicad_footprints_path, path))
        self.DisableNotificationsForPath(configuration.kicad_footprints_path, action=action)
 
        log.info(f"folder '{path}' removed")
        

    @staticmethod
    def RenameFootprint(footprint, newname):
        for f in footprint.Library.Footprints:
            if newname==f.Name:
                raise KicadFileManagerException(f"Footprint '{newname}' already exists in library '{footprint.Library.Path}'")

        if footprint.footprint_file is not None:
            abspath = footprint.footprint_file.AbsPath
            footprint.footprint_file._name = newname
            footprint.footprint_file.Save()
            def action():
                os.remove(abspath)
            KicadFootprintLibraryManager.DisableNotificationsForPath(configuration.kicad_footprints_path, action=action)
            
        if footprint.footprint_model is not None:
            footprint.footprint_model.name = newname
            footprint.footprint_model.mtime = footprint.footprint_file.Mtime
            footprint.footprint_model.save()

    @staticmethod
    def RemoveFootprint(footprint):
        if footprint.footprint_file is not None:
            def action():
                os.remove(footprint.footprint_file.AbsPath)
            KicadFootprintLibraryManager.DisableNotificationsForPath(configuration.kicad_footprints_path, action=action)
            
        if footprint.footprint_model is not None:
            footprint.footprint_model.delete()
