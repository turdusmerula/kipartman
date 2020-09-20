from dialogs.panel_footprint_list import PanelFootprintList
import frames.edit_footprint_frame
import os
import helper.tree
import helper.filter
from kicad.kicad_file_manager_footprints import KicadFootprintLibraryManager, KicadFootprintFile, KicadFootprint
import kicad.kicad_file_manager
import api.data.kicad_footprint_library
import api.data.kicad_footprint
from helper.log import log
from builtins import isinstance
import wx

# from dialogs.panel_footprints import PanelFootprints
# from frames.edit_footprint_frame import EditFootprintFrame, EVT_EDIT_FOOTPRINT_APPLY_EVENT, EVT_EDIT_FOOTPRINT_CANCEL_EVENT
# from helper.filter import Filter
# import rest 
# import helper.tree
# import os
# from helper.tree import TreeImageList
# from helper.exception import print_stack
# from configuration import configuration
# import wx
# import re
# import sync
# import json
# from helper.connection import check_backend
# from helper.profiler import Trace

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
        filters = self.filters.get_filters()
        for library in self.library_manager.Libraries:
            filter = False
            for f in self.filters.get_filters():
                filter = filter or f.apply(library)
            if filter==False:
                res.append(library)
        return res
    
    def LoadFlat(self):
        for library in self._get_libraries():
            for footprint in library.Footprints:
                footprintobj = self.FindFootprint(footprint)
                if footprintobj is None:
                    footprintobj = self.AppendFootprint(None, footprint)
                else:
                    footprintobj.footprint = footprint
                    self.Update(footprintobj)
    
    def LoadTree(self):
        for library in self._get_libraries():
            libraryobj = self.FindLibrary(library)
            if libraryobj is None:
                libraryobj = self.AppendLibrary(library)
            else:
                libraryobj.library = library
                self.Update(libraryobj)
                
            for footprint in library.Footprints:
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
 
class FilterLibraryPath(api.data.kicad_footprint.FilterPath):
    def __init__(self, path):
        super(FilterLibraryPath, self).__init__(path)
    
    def apply(self, request):
        if isinstance(request, kicad.kicad_file_manager_footprints.KicadLibrary):
            return request.Path.startswith(self.path)==False
        else:
            return super(FilterLibraryPath, self).apply(request)

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
        self.tree_footprints_manager = TreeManagerFootprints(self.tree_footprints, context_menu=self.menu_footprints, filters=self.Filters, library_manager=self.library_manager)
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
    
    
    def onFileLibChanged(self, event):
        # do a synchronize when a file change on disk
        self.tree_footprints_manager.Load()

    def onButtonRefreshFootprintsClick( self, event ):
        self.library_manager.Reload()
        self.tree_footprints_manager.Load()

    def onTreeModelsBeforeContextMenu( self, event ):
        item = self.tree_footprints.GetSelection()
        if item.IsOk()==False:
            return    
        obj = self.tree_footprints_manager.ItemToObject(item)
 
        self.menu_footprints_add.Enable(True)
        self.menu_footprints_delete.Enable(True)
        self.menu_footprints_edit.Enable(True)
        if isinstance(obj, Footprint):
            self.menu_footprints_add.Enable(False)
        else:
            self.menu_footprints_delete.Enable(False)
            self.menu_footprints_edit.Enable(False)

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

    def onToggleFootprintPathClicked( self, event ):
        self.Flat = not self.toolbar_footprint.GetToolState(self.toggle_footprint_path.GetId())
        event.Skip()

    def onFilterChanged( self, event ):
        self.tree_footprints_manager.Load()
        self._expand_libraries()
        event.Skip()

    def onMenuFootprintsAdd( self, event ):
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

    def onMenuFootprintsEdit( self, event ):
        event.Skip()

    def onMenuFootprintsDelete( self, event ):
        event.Skip()
# 
    def onEditFootprintApply( self, event ):
        pass

    def onSearchFootprintsCancel( self, event ):
        event.Skip()

    def onSearchFootprintsButton( self, event ):
        event.Skip()

    def onSearchFootprintsTextEnter( self, event ):
        event.Skip()

#         footprint = event.data
#         footprint_name = event.footprint_name
#                 
#         if self.edit_state=='add':
#             # get library path
#             library_path = ''
#             footprint_path = os.path.join(footprint.source_path, footprint_name)
#             try:
#                 self.manager_lib.CreateFile(footprint_path, footprint.content)
#             except Exception as e:
#                 print_stack()
#                 wx.MessageBox(format(e), 'Error creating footprint', wx.OK | wx.ICON_ERROR)                                    
#                 return
#             
#         elif self.edit_state=='edit':
#             # change library name if changed on disk
#             library_path = os.path.dirname(footprint.source_path)
#             footprint_path = os.path.normpath(os.path.join(library_path, footprint_name))
#             
#             if os.path.normpath(footprint.source_path)!=footprint_path:
#                 # file was renamed
#                 if self.tree_footprints.GetSelection().IsOk():
#                     footprintobj = self.tree_footprints_manager.ItemToObject(self.tree_footprints.GetSelection())
#                     try:
#                         footprintobj.footprint = self.manager_lib.MoveFile(footprint.source_path, os.path.join(library_path, footprint_name))
#                     except Exception as e:
#                         print_stack()
#                         wx.MessageBox(format(e), 'Error renaming footprint', wx.OK | wx.ICON_ERROR)                                    
#                         return
#             try:
#                 if footprint.content:
#                     self.manager_lib.EditFile(footprint_path, footprint.content, create=True)
#             except Exception as e:
#                 print_stack()
#                 wx.MessageBox(format(e), 'Error editing footprint', wx.OK | wx.ICON_ERROR)                                    
#                 return
#             
#         else:
#             return
#         
#         self.manager_lib.EditMetadata(footprint_path, footprint.metadata)
#         
#         self.edit_state = None
#         self.show_footprint(footprint)
# 
#         self.load()
# 
    def onEditFootprintCancel( self, event ):
        self.tree_footprints_manager.Load()
        
        # reload the part after changing it
        item = self.tree_footprints.GetSelection()
        obj = self.tree_footprints_manager.ItemToObject(item)
        if isinstance(obj, Footprint):
            self.SetFootprint(obj.footprint)
        else:
            self.SetFootprint(None)

        self.EditMode = False        
        event.Skip()
