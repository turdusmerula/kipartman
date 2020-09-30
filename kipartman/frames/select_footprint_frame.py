from dialogs.panel_select_footprint import PanelSelectFootprint
import helper.tree
import wx
import os
from kicad.kicad_file_manager_footprints import KicadFootprintLibraryManager
import kicad.kicad_file_manager
from kicad import kicad_lib_file
import tempfile
from helper.exception import print_stack
from helper.log import log

class Library(helper.tree.TreeContainerItem):
    def __init__(self, library):
        super(Library, self).__init__()
        self.library = library
    
    @property
    def Path(self):
        return self.library.Path
    
    def GetValue(self, col):
        if col==0:
            return self.library.Path
        return ''

    def HasContainerColumns(self):
        return True

    def GetAttr(self, col, attr):
        if col==0:
            attr.Bold = True
            return True
        return False
    
class Footprint(helper.tree.TreeItem):
    def __init__(self, footprint):
        super(Footprint, self).__init__()
        self.footprint = footprint
            
    def GetValue(self, col):
        if col==0:
            return self.footprint.Name

        return ""


class TreeManagerFootprints(helper.tree.TreeManager):
    def __init__(self, tree_view, *args, filters, library_manager , **kwargs):
        super(TreeManagerFootprints, self).__init__(tree_view, *args, **kwargs)

        self.library_manager = library_manager
        self.filters = filters

        self.AddTextColumn("Name")

    def Load(self):
         
        self.SaveState()
        
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
    
    def AppendLibrary(self, path):
        libraryobj = Library(path)
        self.Append(None, libraryobj)
        return libraryobj

    def FindLibrary(self, library):
        for data in self.data:
            if isinstance(data, Library) and data.library.Path==library.Path:
                return data
        return None

    def FindFootprint(self, footprint):
        for data in self.data:
            if isinstance(data, Footprint) and data.footprint.Name==footprint.Name and data.footprint.Library.Path==footprint.Library.Path:
                return data
        return None

    def AppendFootprint(self, library, footprint):
        libraryobj = None
        if library is not None:
            libraryobj = self.FindLibrary(library)
        footprintobj = Footprint(footprint)
        self.Append(libraryobj, footprintobj)
        return footprintobj


class SelectFootprintFrame(PanelSelectFootprint):
    def __init__(self, parent, initial=None): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(SelectFootprintFrame, self).__init__(parent)
        
        # react to file change
        self.library_manager = KicadFootprintLibraryManager(self)
        self.Bind( kicad.kicad_file_manager.EVT_FILE_CHANGED, self.onFileLibChanged )

        # footprints filters
        self._filters = helper.filter.FilterSet(self)
        self._filters.Bind( helper.filter.EVT_FILTER_CHANGED, self.onFilterChanged )

        # create footprints list
        self.tree_footprints_manager = TreeManagerFootprints(self.tree_footprints, filters=self._filters, library_manager=self.library_manager)
        self.tree_footprints_manager.OnSelectionChanged = self.onTreeFootprintsSelectionChanged
        
        self.search_filter = None
        self.search_footprint.Value = ''
        
        if initial:
            self.tree_footprints_manager.Select(self.tree_footprints_manager.FindFootprint(initial))
        
        # set result functions
        self.cancel = None
        self.result = None

        # initial state
        self.button_footprint_editOK.Enabled = False
        
        self.tree_footprints_manager.Clear()
        self.tree_footprints_manager.Load()

    def onFileLibChanged(self, event):
        # do a synchronize when a file change on disk
        self.tree_footprints_manager.Load()

    def onFilterChanged(self, event):
        # do a synchronize when a filter changed
        self.tree_footprints_manager.Load()

    def SetResult(self, result, cancel=None):
        self.result = result
        self.cancel = cancel
        
    # Virtual event handlers, overide them in your derived class
    def onTreeFootprintsSelectionChanged( self, event ):
        item = self.tree_footprints.GetSelection()
        if item.IsOk()==False:
            return    
        obj = self.tree_footprints_manager.ItemToObject(item)

        if isinstance(obj, Footprint):
#             if obj.footprint.Content!='':
#                 lib = kicad_lib_file.KicadLibFile()
#                 lib.Load(obj.footprint.Content)
#                 image_file = tempfile.NamedTemporaryFile()
#                 lib.Render(image_file.name, self.panel_image_footprint.GetRect().width, self.panel_image_footprint.GetRect().height)
#                 img = wx.Image(image_file.name, wx.BITMAP_TYPE_ANY)
#                 image_file.close()
            self.button_footprint_editOK.Enabled = True
        else:
#             img = wx.Image()
#             img.Create(1, 1)
            self.button_footprint_editOK.Enabled = False
# 
#         img = img.ConvertToBitmap()
#         self.image_footprint.SetBitmap(img)
    
    def onButtonCancelClick( self, event ):
        if self.cancel:
            self.cancel()
    
    def onButtonOkClick( self, event ):
        footprint = self.tree_footprints_manager.ItemToObject(self.tree_footprints.GetSelection())
        if isinstance(footprint, Footprint) and self.result:
            self.result(footprint.footprint)

    def onSearchFootprintCancel( self, event ):
        self.search_filter = None
        self.load()
    
    def onSearchFootprintButton( self, event ):
        self.search_filter = self.search_footprint.Value
        self.load()
    
    def onSearchFootprintEnter( self, event ):
        self.search_filter = self.search_footprint.Value
        self.load()

    def onButtonRefreshFootprintsClick( self, event ):
        self.tree_footprints_manager.Load()
        event.Skip()
