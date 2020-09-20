from dialogs.panel_footprint_libraries import PanelFootprintLibraries
# from frames.edit_footprint_frame import EditFootprintFrame, EVT_EDIT_FOOTPRINT_APPLY_EVENT, EVT_EDIT_FOOTPRINT_CANCEL_EVENT
from kicad.kicad_file_manager_footprints import KicadFootprintLibraryManager
import kicad.kicad_file_manager
import helper.tree
import os
import api.data.kicad_footprint_library
import wx
from helper.exception import print_stack
from helper.log import log
import kicad

class LibraryPath(helper.tree.TreeContainerItem):
    def __init__(self, path):
        super(LibraryPath, self).__init__()
        self.path = path
    
    @property
    def Path(self):
        return self.path
    
    def GetValue(self, col):
        if col==0:
            return os.path.basename(self.path)

        return ""
 
    def GetAttr(self, col, attr):
        attr.Bold = True
        return True
 
    def GetDragData(self):
        return {'id': self.path}

class Library(helper.tree.TreeContainerItem):
    def __init__(self, library):
        super(Library, self).__init__()
        self.library = library
    
    @property
    def Path(self):
        return self.library.Path
    
    def GetValue(self, col):
        if col==0:
            return os.path.basename(self.Path)

        return ""
 
    def GetAttr(self, col, attr):
        attr.Bold = False
        return True
 
    def GetDragData(self):
        return {'id': self.path}
    
class TreeManagerLibraries(helper.tree.TreeManager):
    def __init__(self, tree_view, *args, library_manager, **kwargs):
        super(TreeManagerLibraries, self).__init__(tree_view, *args, **kwargs)
        
        self.library_manager = library_manager
        
    def Load(self):
         
        self.SaveState()
        
        self.library_manager.Load()
        
        for folder in self.library_manager.Folders:
            pathobj = self.FindPath(folder)
            if pathobj is None:
                pathobj = self.AppendPath(folder)
            else:
                self.Update(pathobj)
        
        for library in self.library_manager.Libraries:
            path, file = os.path.split(library.Path)
            
            libraryobj = self.FindLibrary(library.Path)
            if libraryobj is None:
                libraryobj = self.AppendFileLibrary(library)
            else:
                libraryobj.disk_file = library
                self.Update(libraryobj)
            
        self.PurgeState()

    def FindPath(self, path):
        for data in self.data:
            if isinstance(data, LibraryPath) and data.path==os.path.normpath(path):
                return data
        return None
 
    def FindLibrary(self, path):
        for data in self.data:
            if isinstance(data, Library) and data.Path==path:
                return data
        return None
 
    def AppendPath(self, path):
        pathobj = self.FindPath(path)
        if pathobj:
            return pathobj
        pathobj = LibraryPath(path)
        parentpath = self.FindPath(os.path.dirname(path))
        self.Append(parentpath, pathobj)
        return pathobj
 
    def AppendFileLibrary(self, library):
        pathobj = self.FindPath(os.path.dirname(library.Path))
        libraryobj = Library(library=library)
        self.Append(pathobj, libraryobj)

    def AppendStoredLibrary(self, library):
        pathobj = self.FindPath(os.path.dirname(library.path))
        libraryobj = Library(stored_file=library)
        self.Append(pathobj, libraryobj)

(SelectLibraryEvent, EVT_SELECT_LIBRARY) = wx.lib.newevent.NewEvent()

class FootprintLibrariesFrame(PanelFootprintLibraries): 
    def __init__(self, *args, **kwargs):
        super(FootprintLibrariesFrame, self).__init__(*args, **kwargs)

        # react to file change 
        self.library_manager = KicadFootprintLibraryManager(self)
        self.Bind( kicad.kicad_file_manager.EVT_FILE_CHANGED, self.onFileLibChanged )

        # create libraries data
        self.tree_libraries_manager = TreeManagerLibraries(self.tree_libraries, context_menu=self.menu_libraries, library_manager=self.library_manager)
#         self.tree_libraries_manager.AddBitmapColumn("s")
        self.tree_libraries_manager.AddTextColumn("name")
        self.tree_libraries_manager.OnSelectionChanged = self.onTreeLibrariesSelChanged
        self.tree_libraries_manager.OnItemBeforeContextMenu = self.onTreeLibrariesBeforeContextMenu
#     
        self.loaded = False
        
    def activate(self):
        if self.loaded==False:
            self.tree_libraries_manager.Clear()
            self.tree_libraries_manager.Load()
        self.loaded = False
        
    def onFileLibChanged(self, event):
        # do a synchronize when a file change on disk
        self.tree_libraries_manager.Load()

    def onButtonRefreshLibrariesClick( self, event ):
        self.library_manager.Reload()
        self.tree_libraries_manager.Load()
        
    def onTreeLibrariesSelChanged( self, event ):
        item = self.tree_libraries.GetSelection()
        obj = self.tree_libraries_manager.ItemToObject(item)
        path = ''
        if obj is not None:
            path = obj.Path
        wx.PostEvent(self, SelectLibraryEvent(path=path))

    def onMenuLibrariesAddFolder( self, event ):
        item = self.tree_libraries.GetSelection()
        pathobj = self.tree_libraries_manager.ItemToObject(item)
        if isinstance(pathobj, Library):
            pathobj = pathobj.parent
        
        path = ''
        if pathobj is not None:
            path = pathobj.Path
            
        dlg = wx.TextEntryDialog(self, 'Enter folder name', 'Add folder')
        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue()
            try:
                self.library_manager.CreateFolder(os.path.join(path, name))
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), 'Error creating folder', wx.OK | wx.ICON_ERROR)
                dlg.Destroy()
                return
            
            self.library_manager.Reload()
            self.tree_libraries_manager.Load()
            
            # select created item
            pathobj = self.tree_libraries_manager.FindPath(os.path.join(path, name))
            if pathobj is not None:
                self.tree_libraries_manager.Select(pathobj)
        
        dlg.Destroy()

         
        event.Skip()

    def onMenuLibrariesAddLibrary( self, event ):
        item = self.tree_libraries.GetSelection()
        pathobj = self.tree_libraries_manager.ItemToObject(item)
        if isinstance(pathobj, Library):
            pathobj = pathobj.parent

        path = ''
        if pathobj is not None:
            path = pathobj.Path
 
        dlg = wx.TextEntryDialog(self, 'Enter library name', 'Add library')
        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue()
            try:
                library = self.library_manager.CreateLibrary(os.path.join(path, name+".lib"))
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), 'Error creating library', wx.OK | wx.ICON_ERROR)
                dlg.Destroy()
                return

            self.library_manager.Reload()
            self.tree_libraries_manager.Load()
            
            # select created item
            libraryobj = self.tree_libraries_manager.FindLibrary(library.Path)
            if libraryobj is not None:
                self.tree_libraries_manager.Select(libraryobj)
        dlg.Destroy()
        
        event.Skip()

    def onMenuLibrariesRename( self, event ):
        item = self.tree_libraries.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_libraries_manager.ItemToObject(item)
 
        if isinstance(obj, LibraryPath):
            dlg = wx.TextEntryDialog(self, 'Enter new folder name', 'Rename folder')
            if dlg.ShowModal() == wx.ID_OK:
                name = dlg.GetValue()
                try:
                    path = obj.path 
                    newpath = os.path.join(os.path.dirname(path), name)
                    self.library_manager.MoveFolder(path, newpath)
                except Exception as e:
                    print_stack()
                    wx.MessageBox(format(e), 'Error renaming folder', wx.OK | wx.ICON_ERROR)
                    dlg.Destroy()
                    return
            dlg.Destroy()

            self.library_manager.Reload()
            self.tree_libraries_manager.Load()
            
            # select created item
            pathobj = self.tree_libraries_manager.FindPath(newpath)
            if pathobj is not None:
                self.tree_libraries_manager.Select(pathobj)

        elif isinstance(obj, Library):
            dlg = wx.TextEntryDialog(self, 'Enter new library name', 'Rename library')
            if dlg.ShowModal() == wx.ID_OK:
                name = dlg.GetValue()
                try:
                    if name.endswith(".lib")==False:
                        name += ".lib"
                    path = obj.library.Path                     
                    newpath = os.path.join(os.path.dirname(path), name)
                    library = self.library_manager.MoveLibrary(obj.library, newpath)
                except Exception as e:
                    print_stack()
                    wx.MessageBox(format(e), 'Error renaming library', wx.OK | wx.ICON_ERROR)
                    dlg.Destroy()
                    return
            dlg.Destroy()

            self.library_manager.Reload()
            self.tree_libraries_manager.Load()

            # select created item
            libraryobj = self.tree_libraries_manager.FindLibrary(library.Path)
            if libraryobj is not None:
                self.tree_libraries_manager.Select(libraryobj)

        event.Skip()

    def onMenuLibrariesRemove( self, event ):
        item = self.tree_libraries.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_libraries_manager.ItemToObject(item)
        
        remove_path = None
        if isinstance(obj, LibraryPath):
            path = obj.path
            remove_path = path
        elif isinstance(obj, Library):
            path = obj.library.Path
            
        libraries_to_remove = []
        for library in self.library_manager.Libraries:
            if library.Path==path:
                libraries_to_remove.append(library)
            elif library.Path.startswith(path+os.sep):
                libraries_to_remove.append(library)

        footprints_to_remove = []
        for library in libraries_to_remove:
            for footprint in library.Footprints:
                footprints_to_remove.append(footprint.footprint_model)
        
        associated_parts = api.data.part.find([api.data.part.FilterFootprints(footprints_to_remove)])
        if len(associated_parts.all())>0:
            dlg = wx.MessageDialog(self, f"There is {len(associated_parts.all())} parts associated with selection, remove anyway?", 'Remove', wx.YES_NO | wx.ICON_EXCLAMATION)
        else:
            dlg = wx.MessageDialog(self, f"Remove selection?", 'Remove', wx.YES_NO | wx.ICON_EXCLAMATION)
        if dlg.ShowModal()==wx.ID_YES:
            try:
                for library in libraries_to_remove:
                    self.library_manager.DeleteLibrary(library)
                if remove_path is not None:
                    self.library_manager.DeleteFolder(path)
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), 'Error removing %s:'%path, wx.OK | wx.ICON_ERROR)
                dlg.Destroy()
                return

            self.library_manager.Reload()
            self.tree_libraries_manager.Load()

        dlg.Destroy()

    def onMenuLibrariesAddFootprint( self, event ):
        item = self.tree_libraries.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_libraries_manager.ItemToObject(item)
        if isinstance(obj, Library)==False:
            return
# 
#         self.edit_state = 'add'
#         self.new_footprint(obj.path)
        event.Skip()

    def onTreeLibrariesBeforeContextMenu( self, event ):
        item = self.tree_libraries.GetSelection()
        if item.IsOk()==False:
            return    
        obj = self.tree_libraries_manager.ItemToObject(item)

        self.menu_libraries_add_folder.Enable(True)
        self.menu_libraries_add_library.Enable(True)
        self.menu_libraries_add_footprint.Enable(True)
        if isinstance(obj, Library)==False:
            self.menu_libraries_add_footprint.Enable(False)

        event.Skip()
