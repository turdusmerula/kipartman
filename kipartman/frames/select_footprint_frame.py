from dialogs.panel_select_footprint import PanelSelectFootprint
import helper.tree
import wx
import os
from kicad.kicad_file_manager import KicadFileManagerPretty
from kicad import kicad_mod_file
import sync.version_manager
from configuration import Configuration
import tempfile

class DataModelFootprintPath(helper.tree.TreeContainerItem):
    def __init__(self, path):
        super(DataModelFootprintPath, self).__init__()
        self.path = path
        
    def GetValue(self, col):
        if col==0:
            return self.path
        return ''

    def HasContainerColumns(self):
        return True

    def GetAttr(self, col, attr):
        if col==0:
            attr.Bold = True
            return True
        return False

class DataModelFootprint(helper.tree.TreeItem):
    def __init__(self, footprint):
        super(DataModelFootprint, self).__init__()
        self.footprint = footprint

    def GetValue(self, col):
        name = os.path.basename(self.footprint.source_path).replace(".kicad_mod", "")
        vMap = {
            0 : name, 
        }
        return vMap[col]


class TreeManagerFootprints(helper.tree.TreeManager):
    def __init__(self, tree_view):
        super(TreeManagerFootprints, self).__init__(tree_view)

    def FindPath(self, path):
        for data in self.data:
            if isinstance(data, DataModelFootprintPath) and data.path==os.path.normpath(path):
                return data
        return None

    def AppendPath(self, path):
        pathobj = self.FindPath(path)
        if pathobj:
            return pathobj
        pathobj = DataModelFootprintPath(path)
        parentpath = self.FindPath(os.path.dirname(path))
        self.AppendItem(parentpath, pathobj)
        return pathobj

    def FindFootprint(self, path):
        for data in self.data:
            if isinstance(data, DataModelFootprint) and data.footprint.source_path==os.path.normpath(path):
                return data
        return None

    def AppendFootprint(self, file):
        footprintobj = self.FindFootprint(file.source_path)
        if footprintobj:
            return footprintobj
        path = os.path.dirname(os.path.normpath(file.source_path))
        pathobj = self.FindPath(path)
        footprintobj = DataModelFootprint(file)
        self.AppendItem(pathobj, footprintobj)
        return footprintobj


class SelectFootprintFrame(PanelSelectFootprint):
    def __init__(self, parent, initial=None): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(SelectFootprintFrame, self).__init__(parent)

        self.file_manager_pretty = KicadFileManagerPretty()
        self.manager_pretty = sync.version_manager.VersionManager(self.file_manager_pretty)
        self.manager_pretty.on_change_hook = self.onFilePrettyChanged
        
        # create footprints list
        self.tree_footprints_manager = TreeManagerFootprints(self.tree_footprints)
        self.tree_footprints_manager.AddTextColumn("Name")
        
        self.search_filter = None
        self.search_footprint.Value = ''
        self.load()
        
        if initial:
            self.tree_footprints.Select(self.tree_footprints_manager.ObjectToItem(self.tree_footprints_manager.FindFootprint(initial.id)))
        
        # set result functions
        self.cancel = None
        self.result = None

    def load(self):
        try:
            self.loadFootprints()
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def loadFootprints(self):
        # clear all
        self.tree_footprints_manager.ClearItems()
        
        self.manager_pretty.LoadState()
        
        # add folders with no library inside
        # only versioned files are available from list
        for file in self.file_manager_pretty.files:
            filename = os.path.basename(file)
            path = os.path.dirname(os.path.normpath(file))
            file_version = self.manager_pretty.GetFile(file)
            if file_version and file_version.id:
                filtered = False
                if self.search_filter and file_version.source_path.find(self.search_filter)!=-1:
                    filtered = False
                elif self.search_filter:
                    filtered = True
                if filtered==False:
                    pathobj = None
                    if path!='':
                        pathobj = self.tree_footprints_manager.AppendPath(path)
                    self.tree_footprints_manager.AppendFootprint(file_version)

    def onFilePrettyChanged(self, event):
        # do a synchronize when a file change on disk
        self.load()

    def SetResult(self, result, cancel=None):
        self.result = result
        self.cancel = cancel
        
    # Virtual event handlers, overide them in your derived class
    def onTreeFootprintsSelectionChanged( self, event ):
        configuration = Configuration()

        item = self.tree_footprints.GetSelection()
        if item.IsOk()==False:
            return    
        obj = self.tree_footprints_manager.ItemToObject(item)

        if isinstance(obj, DataModelFootprint):
            if os.path.exists(os.path.join(configuration.kicad_footprints_path, obj.footprint.source_path)):
                mod = kicad_mod_file.KicadModFile()
                mod.LoadFile(os.path.join(configuration.kicad_footprints_path, obj.footprint.source_path))
                image_file = tempfile.NamedTemporaryFile()
                mod.Render(image_file.name, self.panel_image_footprint.GetRect().width, self.panel_image_footprint.GetRect().height)
                img = wx.Image(image_file.name, wx.BITMAP_TYPE_ANY)
                image_file.close()
            else:
                img = wx.Image()
                img.Create(1, 1)
        else:
            img = wx.Image()
            img.Create(1, 1)

        img = img.ConvertToBitmap()
        self.image_footprint.SetBitmap(img)
    
    def onButtonCancelClick( self, event ):
        if self.cancel:
            self.cancel()
    
    def onButtonOkClick( self, event ):
        footprint = self.tree_footprints_manager.ItemToObject(self.tree_footprints.GetSelection())
        if isinstance(footprint, DataModelFootprint) and self.result:
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
