from dialogs.panel_select_symbol import PanelSelectSymbol
import helper.tree
import wx
import os
from kicad.kicad_file_manager import KicadFileManagerPretty, KicadFileManagerLib
from kicad import kicad_lib_file
import sync.version_manager
import tempfile

class DataModelSymbolPath(helper.tree.TreeContainerItem):
    def __init__(self, path):
        super(DataModelSymbolPath, self).__init__()
        self.path = path
    
    def GetValue(self, col):
        if col==0:
            return self.path
        return ''

    def HasContainerColumns(self):
        return True

    def GetAttr(self, col, attr):
        if col==1:
            attr.Bold = True
            return True
        return False
    
class DataModelSymbol(helper.tree.TreeItem):
    def __init__(self, symbol):
        super(DataModelSymbol, self).__init__()
        self.symbol = symbol
            
    def GetValue(self, col):
        name = os.path.basename(self.symbol.source_path).replace(".mod", "")
        vMap = {
            0 : name, 
        }
        return vMap[col]


class TreeManagerSymbols(helper.tree.TreeManager):
    def __init__(self, tree_view):
        super(TreeManagerSymbols, self).__init__(tree_view)

    def FindPath(self, path):
        for data in self.data:
            if isinstance(data, DataModelSymbolPath) and data.path==os.path.normpath(path):
                return data
        return None

    def AppendPath(self, path):
        pathobj = self.FindPath(path)
        if pathobj:
            return pathobj
        pathobj = DataModelSymbolPath(path)
        parentpath = self.FindPath(os.path.dirname(path))
        self.AppendItem(parentpath, pathobj)
        return pathobj

    def FindSymbol(self, path):
        for data in self.data:
            if isinstance(data, DataModelSymbol) and data.symbol.source_path==os.path.normpath(path):
                return data
        return None

    def AppendSymbol(self, file):
        symbolobj = self.FindSymbol(file.source_path)
        if symbolobj:
            return symbolobj
        path = os.path.dirname(os.path.normpath(file.source_path))
        pathobj = self.FindPath(path)
        symbolobj = DataModelSymbol(file)
        self.AppendItem(pathobj, symbolobj)
        return symbolobj


class SelectSymbolFrame(PanelSelectSymbol):
    def __init__(self, parent, initial=None): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(SelectSymbolFrame, self).__init__(parent)
        
        self.file_manager_lib = KicadFileManagerLib()
        self.manager_lib = sync.version_manager.VersionManager(self.file_manager_lib)
        self.manager_lib.on_change_hook = self.onFileLibChanged
        self.lib_cache = KicadFileManagerLib()

        # create symbols list
        self.tree_symbols_manager = TreeManagerSymbols(self.tree_symbols)
        self.tree_symbols_manager.AddTextColumn("Name")
        
        self.search_filter = None
        self.search_symbol.Value = ''
        self.load()
        
        if initial:
            self.tree_symbols.Select(self.tree_symbols_manager.ObjectToItem(self.tree_symbols_manager.FindSymbol(initial.id)))
        
        # set result functions
        self.cancel = None
        self.result = None

    def load(self):
        try:
            self.loadSymbols()
            pass
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def loadSymbols(self):
        # clear all
        self.tree_symbols_manager.ClearItems()
        
        self.manager_lib.LoadState()
        
        # add folders with no library inside
        # only versioned files are available from list
        for file in self.file_manager_lib.files:
            path = os.path.dirname(os.path.normpath(file))
            file_version = self.manager_lib.GetFile(file)
            if file_version and file_version.id:
                filtered = False
                if self.search_filter and file_version.source_path.find(self.search_filter)!=-1:
                    filtered = False
                elif self.search_filter:
                    filtered = True
                if filtered==False:
                    if path!='':
                        self.tree_symbols_manager.AppendPath(path)
                    self.tree_symbols_manager.AppendSymbol(file_version)

    def onFileLibChanged(self, event):
        # do a synchronize when a file change on disk
        self.load()

    def SetResult(self, result, cancel=None):
        self.result = result
        self.cancel = cancel
        
    # Virtual event handlers, overide them in your derived class
    def onTreeSymbolsSelectionChanged( self, event ):
        item = self.tree_symbols.GetSelection()
        if item.IsOk()==False:
            return    
        obj = self.tree_symbols_manager.ItemToObject(item)

        if isinstance(obj, DataModelSymbol):
            print "----", obj.symbol.source_path
            if self.lib_cache.Exists(obj.symbol.source_path):
                self.lib_cache.LoadContent(obj.symbol)
                lib = kicad_lib_file.KicadLibFile()
                lib.Load(obj.symbol.content)
                image_file = tempfile.NamedTemporaryFile()
                lib.Render(image_file.name, self.panel_image_symbol.GetRect().width, self.panel_image_symbol.GetRect().height)
                img = wx.Image(image_file.name, wx.BITMAP_TYPE_ANY)
                image_file.close()
            else:
                img = wx.Image()
                img.Create(1, 1)
        else:
            img = wx.Image()
            img.Create(1, 1)

        img = img.ConvertToBitmap()
        self.image_symbol.SetBitmap(img)
    
    def onButtonCancelClick( self, event ):
        if self.cancel:
            self.cancel()
    
    def onButtonOkClick( self, event ):
        symbol = self.tree_symbols_manager.ItemToObject(self.tree_symbols.GetSelection())
        if isinstance(symbol, DataModelSymbol) and self.result:
            self.result(symbol.symbol)

    def onSearchSymbolCancel( self, event ):
        self.search_filter = None
        self.load()
    
    def onSearchSymbolButton( self, event ):
        self.search_filter = self.search_symbol.Value
        self.load()
    
    def onSearchSymbolEnter( self, event ):
        self.search_filter = self.search_symbol.Value
        self.load()
