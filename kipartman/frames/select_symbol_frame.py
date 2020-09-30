from dialogs.panel_select_symbol import PanelSelectSymbol
import helper.tree
import wx
import os
from kicad.kicad_file_manager_symbols import KicadSymbolLibraryManager
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
    
class Symbol(helper.tree.TreeItem):
    def __init__(self, symbol):
        super(Symbol, self).__init__()
        self.symbol = symbol
            
    def GetValue(self, col):
        if col==0:
            return self.symbol.Name

        return ""


class TreeManagerSymbols(helper.tree.TreeManager):
    def __init__(self, tree_view, *args, filters, library_manager , **kwargs):
        super(TreeManagerSymbols, self).__init__(tree_view, *args, **kwargs)

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
                
            for symbol in library.Symbols:
                symbolobj = self.FindSymbol(symbol)
                if symbolobj is None:
                    symbolobj = self.AppendSymbol(libraryobj, symbol)
                else:
                    symbolobj.symbol = symbol
                    self.Update(symbolobj)
        
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

    def FindSymbol(self, symbol):
        for data in self.data:
            if isinstance(data, Symbol) and data.symbol.Name==symbol.Name and data.symbol.Library.Path==symbol.Library.Path:
                return data
        return None

    def AppendSymbol(self, library, symbol):
        libraryobj = None
        if library is not None:
            libraryobj = self.FindLibrary(library)
        symbolobj = Symbol(symbol)
        self.Append(libraryobj, symbolobj)
        return symbolobj


class SelectSymbolFrame(PanelSelectSymbol):
    def __init__(self, parent, initial=None): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(SelectSymbolFrame, self).__init__(parent)
        
        # react to file change
        self.library_manager = KicadSymbolLibraryManager(self)
        self.Bind( kicad.kicad_file_manager.EVT_FILE_CHANGED, self.onFileLibChanged )

        # symbols filters
        self._filters = helper.filter.FilterSet(self)
        self._filters.Bind( helper.filter.EVT_FILTER_CHANGED, self.onFilterChanged )

        # create symbols list
        self.tree_symbols_manager = TreeManagerSymbols(self.tree_symbols, filters=self._filters, library_manager=self.library_manager)
        self.tree_symbols_manager.OnSelectionChanged = self.onTreeSymbolsSelectionChanged
        
        self.search_filter = None
        self.search_symbol.Value = ''
        
        if initial:
            self.tree_symbols_manager.Select(self.tree_symbols_manager.FindSymbol(initial))
        
        # set result functions
        self.cancel = None
        self.result = None

        # initial state
        self.button_symbol_editOK.Enabled = False
        
        self.tree_symbols_manager.Clear()
        self.tree_symbols_manager.Load()

    def onFileLibChanged(self, event):
        # do a synchronize when a file change on disk
        self.tree_symbols_manager.Load()

    def onFilterChanged(self, event):
        # do a synchronize when a filter changed
        self.tree_symbols_manager.Load()

    def SetResult(self, result, cancel=None):
        self.result = result
        self.cancel = cancel
        
    # Virtual event handlers, overide them in your derived class
    def onTreeSymbolsSelectionChanged( self, event ):
        item = self.tree_symbols.GetSelection()
        if item.IsOk()==False:
            return    
        obj = self.tree_symbols_manager.ItemToObject(item)

        if isinstance(obj, Symbol):
#             if obj.symbol.Content!='':
#                 lib = kicad_lib_file.KicadLibFile()
#                 lib.Load(obj.symbol.Content)
#                 image_file = tempfile.NamedTemporaryFile()
#                 lib.Render(image_file.name, self.panel_image_symbol.GetRect().width, self.panel_image_symbol.GetRect().height)
#                 img = wx.Image(image_file.name, wx.BITMAP_TYPE_ANY)
#                 image_file.close()
            self.button_symbol_editOK.Enabled = True
        else:
#             img = wx.Image()
#             img.Create(1, 1)
            self.button_symbol_editOK.Enabled = False

#         img = img.ConvertToBitmap()
#         self.image_symbol.SetBitmap(img)
    
    def onButtonCancelClick( self, event ):
        if self.cancel:
            self.cancel()
    
    def onButtonOkClick( self, event ):
        symbol = self.tree_symbols_manager.ItemToObject(self.tree_symbols.GetSelection())
        if isinstance(symbol, Symbol) and self.result:
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

    def onButtonRefreshSymbolsClick( self, event ):
        self.tree_symbols_manager.Load()
        event.Skip()
