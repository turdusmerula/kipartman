from dialogs.panel_footprint_list import PanelFootprintList
import frames.edit_footprint_frame
from kicad.kicad_file_manager_footprints import KicadFootprintLibraryManager, KicadFootprintFile, KicadFootprint
import kicad.kicad_file_manager
import api.data.kicad_footprint_library
import api.data.kicad_footprint
import wx
import os
import helper.tree
import helper.filter
from helper.log import log
from helper.exception import print_stack
from helper.filter import Filter

class Library(helper.tree.TreeContainerItem):
    def __init__(self, library):
        super(Library, self).__init__()
        self.library = library

    @property
    def Path(self):
        return self.library.Path
    
    def GetValue(self, col):
        if col==0:
            return self.Path
        return ''

    def GetAttr(self, col, attr):
        attr.Bold = True
        return True
 
class Footprint(helper.tree.TreeItem):
    def __init__(self, footprint):
        super(Footprint, self).__init__()
        self.footprint = footprint
 
    def GetValue(self, col):
        if col==0:
            if self.parent is None:
                return os.path.join(self.footprint.Library.Path, self.footprint.Name)
            else:
                return self.footprint.Name
 
        return ''
 
#    def GetDragData(self):
#        if isinstance(self.parent, DataModelCategoryPath):
#            return {'id': self.footprint.id}
#        return None

def cut_path(path):
    res = []
    while len(path)>0:
        path, folder = os.path.split(path)
        res.append(folder)
    res.reverse()

    if len(res)==1 and res[0]=='.':
        return []
    return res

class TreeManagerFootprints(helper.tree.TreeManager):
    def __init__(self, tree_view, *args, filters, library_manager , **kwargs):
        super(TreeManagerFootprints, self).__init__(tree_view, *args, **kwargs)

        self.library_manager = library_manager
        self.filters = filters
        
        self.flat = False

    def Load(self):
         
        self.SaveState()
        
        # reload libraries from disk
        self.library_manager.Load()

        if self.flat:
            self.LoadFlat()
        else:
            self.LoadTree()
        
        self.PurgeState()

    def _get_libraries(self):
        res = []
        filters = self.filters.get_filters_group("path")
        for library in self.library_manager.Libraries:
            filter = False
            for f in filters:
                filter = filter or f.apply(library)
            if filter==False:
                res.append(library)
        return res
    
    def LoadFlat(self):
        filters = self.filters.get_filters()

        for library in self._get_libraries():
            for footprint in library.Footprints:
                filter = False
                for f in filters:
                    filter = filter or f.apply(footprint)
                if filter==False:    
                    footprintobj = self.FindFootprint(footprint)
                    if footprintobj is None:
                        footprintobj = self.AppendFootprint(None, footprint)
                    else:
                        footprintobj.footprint = footprint
                        self.Update(footprintobj)
    
    def LoadTree(self):
        filters = self.filters.get_filters()
        for library in self._get_libraries():
            library_footprints = []
            for footprint in library.Footprints:
                filter = False
                for f in filters:
                    filter = filter or f.apply(footprint)
                if filter==False:
                    library_footprints.append(footprint)
             
            if len(library_footprints)>0:
                libraryobj = self.FindLibrary(library)
                if libraryobj is None:
                    libraryobj = self.AppendLibrary(library)
                else:
                    libraryobj.library = library
                    self.Update(libraryobj)
             
                for footprint in library_footprints:
                    footprintobj = self.FindFootprint(footprint)
                    if footprintobj is None:
                        footprintobj = self.AppendFootprint(libraryobj, footprint)
                    else:
                        footprintobj.footprint = footprint
                        self.Update(footprintobj)
                    
    def FindFootprint(self, footprint):
        for data in self.data:
            if isinstance(data, Footprint) and data.footprint.Name==footprint.Name and data.footprint.Library.Path==footprint.Library.Path:
                return data
        return None

    def FindLibrary(self, library):
        for data in self.data:
            if isinstance(data, Library) and data.library.Path==library.Path:
                return data
        return None
    
    def FindLibraries(self,):
        res = []
        for data in self.data:
            if isinstance(data, Library):
                res.append(data)
        return res
  
    def AppendLibrary(self, path):
        libraryobj = Library(path)
        self.Append(None, libraryobj)
        return libraryobj

    def AppendFootprint(self, library, footprint):
        libraryobj = None
        if library is not None:
            libraryobj = self.FindLibrary(library)
        footprintobj = Footprint(footprint)
        self.Append(libraryobj, footprintobj)
        return footprintobj
 
class FilterLibraryPath(helper.filter.Filter):
    def __init__(self, path):
        self.path = path
        super(FilterLibraryPath, self).__init__()
    
    def apply(self, library):
        if isinstance(library, kicad.kicad_file_manager_footprints.KicadFootprintLibrary):
            return library.Path.startswith(self.path)==False
        return False
    
    def __str__(self):
        return f"path: {self.path}"
    
class FilterTextSearch(helper.filter.Filter):
    def __init__(self, value):
        self.value = value
        super(FilterTextSearch, self).__init__()
    
    def apply(self, footprint):
        if isinstance(footprint, kicad.kicad_file_manager_footprints.KicadFootprint):
            return not ( self.value in footprint.Content or self.value in footprint.Name )
        return False
    
    def __str__(self):
        return f"search: {self.value}"

(EnterEditModeEvent, EVT_ENTER_EDIT_MODE) = wx.lib.newevent.NewEvent()
(ExitEditModeEvent, EVT_EXIT_EDIT_MODE) = wx.lib.newevent.NewEvent()

class FootprintListFrame(PanelFootprintList): 
    def __init__(self, *args, **kwargs):
        super(FootprintListFrame, self).__init__(*args, **kwargs)

        # react to file change
        self.library_manager = KicadFootprintLibraryManager(self)
        self.Bind( kicad.kicad_file_manager.EVT_FILE_CHANGED, self.onFileLibChanged )

        # footprints filters
        self._filters = helper.filter.FilterSet(self, self.toolbar_filters)
        self.Filters.Bind( helper.filter.EVT_FILTER_CHANGED, self.onFilterChanged )

        # create footprint list
        self.tree_footprints_manager = TreeManagerFootprints(self.tree_footprints, context_menu=self.menu_footprint, filters=self.Filters, library_manager=self.library_manager)
        self.tree_footprints_manager.AddTextColumn("name")
        self.tree_footprints_manager.OnSelectionChanged = self.onTreeModelsSelChanged
        self.tree_footprints_manager.OnItemBeforeContextMenu = self.onTreeModelsBeforeContextMenu

        # create edit footprint panel
        self.panel_edit_footprint = frames.edit_footprint_frame.EditFootprintFrame(self.splitter_horz)
        self.panel_edit_footprint.Bind( frames.edit_footprint_frame.EVT_EDIT_FOOTPRINT_APPLY_EVENT, self.onEditFootprintApply )
        self.panel_edit_footprint.Bind( frames.edit_footprint_frame.EVT_EDIT_FOOTPRINT_CANCEL_EVENT, self.onEditFootprintCancel )

        # organize panels
        self.splitter_horz.Unsplit()
        self.splitter_horz.SplitHorizontally( self.panel_up, self.panel_edit_footprint)
        self.panel_down.Hide()

        # initial state
        self.toolbar_footprint.ToggleTool(self.toggle_footprint_path.GetId(), True)
        self.Flat = False
        self.EditMode = False
#     
    @property
    def Filters(self):
        return self._filters

    @property
    def Flat(self):
        return self.tree_footprints_manager.flat
    
    @Flat.setter
    def Flat(self, value):
        self.tree_footprints_manager.flat = value
        self.tree_footprints_manager.Clear()
        self.tree_footprints_manager.Load()
        self._expand_libraries()

    @property
    def EditMode(self):
        return self._edit_mode
    
    @EditMode.setter
    def EditMode(self, value):
        self._edit_mode = value
        if self._edit_mode:
            wx.PostEvent(self, EnterEditModeEvent())        
        else:
            wx.PostEvent(self, ExitEditModeEvent())        
            
    
    def activate(self):
        self.tree_footprints_manager.Load()

    def _expand_libraries(self):
        if self.Flat==False:
            for library in self.tree_footprints_manager.FindLibraries():
                self.tree_footprints_manager.Expand(library)

    def _enable(self, value):
        self.panel_up.Enabled = value


    def SetFootprint(self, footprint):
        self.panel_edit_footprint.SetFootprint(footprint)
        self._enable(True)
        
    def EditFootprint(self, footprint):
        self.EditMode = True
        self.panel_edit_footprint.EditFootprint(footprint)
        self._enable(False)


    
    def onToggleFootprintPathClicked( self, event ):
        self.Flat = not self.toolbar_footprint.GetToolState(self.toggle_footprint_path.GetId())
        event.Skip()

    def onButtonRefreshFootprintsClick( self, event ):
        self.library_manager.Reload()
        self.tree_footprints_manager.Load()

    def onFileLibChanged(self, event):
        # do a synchronize when a file change on disk
        self.tree_footprints_manager.Load()

    def onFilterChanged( self, event ):
        self.tree_footprints_manager.Load()
        self._expand_libraries()
        event.Skip()

    def onTreeModelsSelChanged( self, event ):
        item = self.tree_footprints.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_footprints_manager.ItemToObject(item)
        if isinstance(obj, Footprint)==False:
            self.panel_edit_footprint.SetFootprint(None)
            return
        self.panel_edit_footprint.SetFootprint(obj.footprint)
        event.Skip()

    def onTreeModelsBeforeContextMenu( self, event ):
        item = self.tree_footprints.GetSelection()
        if item.IsOk()==False:
            return    
        obj = self.tree_footprints_manager.ItemToObject(item)
 
        self.menu_footprint_add.Enable(True)
        self.menu_footprint_duplicate.Enable(True)
        self.menu_footprint_remove.Enable(True)
        self.menu_footprint_edit.Enable(True)
        if isinstance(obj, Footprint):
            self.menu_footprint_add.Enable(False)
        else:
            self.menu_footprint_duplicate.Enable(False)
            self.menu_footprint_remove.Enable(False)
            self.menu_footprint_edit.Enable(False)

    def onMenuFootprintAdd( self, event ):
        item = self.tree_footprints.GetSelection()
        library = None
        if item.IsOk():
            obj = self.tree_footprints_manager.ItemToObject(item)
            if isinstance(obj, Library):
                library = obj.library
            elif isinstance(obj, Footprint):
                library = obj.footprint.library
        
        if library is None:
            # TODO
            return
        
        footprint_file = KicadFootprintFile(library.library_file, "", "")
        footprint = KicadFootprint(library, footprint_file=footprint_file)
        
        self.EditFootprint(footprint)
        
        event.Skip()

    def onMenuFootprintDuplicate( self, event ):
        item = self.tree_footprints.GetSelection()
        library = None
        
        event.Skip()

    def onMenuFootprintEdit( self, event ):
        item = self.tree_footprints.GetSelection()
        if not item.IsOk():
            return
        obj = self.tree_footprints_manager.ItemToObject(item)
        if isinstance(obj, Footprint)==False:
            return
        self.EditFootprint(obj.footprint)
        event.Skip()

    def onMenuFootprintRemove( self, event ):
        item = self.tree_footprints.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_footprints_manager.ItemToObject(item)
        
        footprints_to_remove = []
        library_to_remove = None
        if isinstance(obj, Library):
            library_to_remove = obj.library
            for footprint in obj.library.Footprints:
                footprints_to_remove.append(footprint)
        else:
            footprints_to_remove.append(obj.footprint)
        
        associated_parts = api.data.part.find([api.data.part.FilterFootprints(footprint.footprint_model for footprint in footprints_to_remove)])
        if len(associated_parts.all())>0:
            dlg = wx.MessageDialog(self, f"There is {len(associated_parts.all())} parts associated with selection, remove anyway?", 'Remove', wx.YES_NO | wx.ICON_EXCLAMATION)
        else:
            dlg = wx.MessageDialog(self, f"Remove selection?", 'Remove', wx.YES_NO | wx.ICON_EXCLAMATION)
        if dlg.ShowModal()==wx.ID_YES:
            try:
                if library_to_remove is None:
                    for footprint in footprints_to_remove:
                        self.library_manager.RemoveFootprint(footprint)
                else:
                    self.library_manager.RemoveLibrary(library_to_remove)
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), 'Error removing %s:'%path, wx.OK | wx.ICON_ERROR)
                dlg.Destroy()
                return

            self.library_manager.Reload()
            self.tree_footprints_manager.Load()

        dlg.Destroy()
        event.Skip()
# 
    def onEditFootprintApply( self, event ):
        self.tree_footprints_manager.Load()
        self.SetFootprint(event.data)
        event.Skip()

    def onEditFootprintCancel( self, event ):
        self.tree_footprints_manager.Load()

        item = self.tree_footprints.GetSelection()
        obj = self.tree_footprints_manager.ItemToObject(item)
        if isinstance(obj, Footprint):
            self.SetFootprint(obj.footprint)
        else:
            self.SetFootprint(None)
        event.Skip()

    def onSearchFootprintsCancel( self, event ):
        self._filters.remove_group('search')
        event.Skip()

    def onSearchFootprintsButton( self, event ):
        self._filters.replace(FilterTextSearch(self.search_footprints.Value), 'search')
        event.Skip()

    def onSearchFootprintsTextEnter( self, event ):
        self._filters.replace(FilterTextSearch(self.search_footprints.Value), 'search')
        event.Skip()
