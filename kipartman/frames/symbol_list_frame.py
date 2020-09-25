from dialogs.panel_symbol_list import PanelSymbolList
import frames.edit_symbol_frame
from kicad.kicad_file_manager_symbols import KicadSymbolLibraryManager, KicadSymbolFile, KicadSymbol
import kicad.kicad_file_manager
import api.data.kicad_symbol_library
import api.data.kicad_symbol
import os
import wx
import helper.tree
import helper.filter
from helper.log import log
from helper.filter import Filter
from helper.exception import print_stack

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
 
class Symbol(helper.tree.TreeItem):
    def __init__(self, symbol):
        super(Symbol, self).__init__()
        self.symbol = symbol
 
    def GetValue(self, col):
        if col==0:
            if self.parent is None:
                return os.path.join(self.symbol.Library.Path, self.symbol.Name)
            else:
                return self.symbol.Name
 
        return ''
 
#    def GetDragData(self):
#        if isinstance(self.parent, DataModelCategoryPath):
#            return {'id': self.symbol.id}
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

class TreeManagerSymbols(helper.tree.TreeManager):
    def __init__(self, tree_view, *args, filters, library_manager , **kwargs):
        super(TreeManagerSymbols, self).__init__(tree_view, *args, **kwargs)

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
            for symbol in library.Symbols:
                filter = False
                for f in filters:
                    filter = filter or f.apply(symbol)
                if filter==False:    
                    symbolobj = self.FindSymbol(symbol)
                    if symbolobj is None:
                        symbolobj = self.AppendSymbol(None, symbol)
                    else:
                        symbolobj.symbol = symbol
                        self.Update(symbolobj)
    
    def LoadTree(self):
        filters = self.filters.get_filters()
        for library in self._get_libraries():
            library_symbols = []
            for symbol in library.Symbols:
                filter = False
                for f in filters:
                    filter = filter or f.apply(symbol)
                if filter==False:
                    library_symbols.append(symbol)
             
            if len(library_symbols)>0:
                libraryobj = self.FindLibrary(library)
                if libraryobj is None:
                    libraryobj = self.AppendLibrary(library)
                else:
                    libraryobj.library = library
                    self.Update(libraryobj)
             
                for symbol in library_symbols:
                    symbolobj = self.FindSymbol(symbol)
                    if symbolobj is None:
                        symbolobj = self.AppendSymbol(libraryobj, symbol)
                    else:
                        symbolobj.symbol = symbol
                        self.Update(symbolobj)
    
    def FindSymbol(self, symbol):
        for data in self.data:
            if isinstance(data, Symbol) and data.symbol.Name==symbol.Name and data.symbol.Library.Path==symbol.Library.Path:
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

    def AppendSymbol(self, library, symbol):
        libraryobj = None
        if library is not None:
            libraryobj = self.FindLibrary(library)
        symbolobj = Symbol(symbol)
        self.Append(libraryobj, symbolobj)
        return symbolobj
 
class FilterLibraryPath(helper.filter.Filter):
    def __init__(self, path):
        self.path = path
        super(FilterLibraryPath, self).__init__()
    
    def apply(self, library):
        if isinstance(library, kicad.kicad_file_manager_symbols.KicadSymbolLibrary):
            return library.Path.startswith(self.path)==False
        return False
    
    def __str__(self):
        return f"path: {self.path}"
    
class FilterTextSearch(helper.filter.Filter):
    def __init__(self, value):
        self.value = value
        super(FilterTextSearch, self).__init__()
    
    def apply(self, symbol):
        if isinstance(symbol, kicad.kicad_file_manager_symbols.KicadSymbol):
            return not ( self.value in symbol.Content or self.value in symbol.Metadata or self.value in symbol.Name )
        return False
    
    def __str__(self):
        return f"search: {self.value}"

(EnterEditModeEvent, EVT_ENTER_EDIT_MODE) = wx.lib.newevent.NewEvent()
(ExitEditModeEvent, EVT_EXIT_EDIT_MODE) = wx.lib.newevent.NewEvent()

class SymbolListFrame(PanelSymbolList): 
    def __init__(self, *args, **kwargs):
        super(SymbolListFrame, self).__init__(*args, **kwargs)

        # react to file change
        self.library_manager = KicadSymbolLibraryManager(self)
        self.Bind( kicad.kicad_file_manager.EVT_FILE_CHANGED, self.onFileLibChanged )

        # symbols filters
        self._filters = helper.filter.FilterSet(self, self.toolbar_filters)
        self.Filters.Bind( helper.filter.EVT_FILTER_CHANGED, self.onFilterChanged )

        # create symbol list
        self.tree_symbols_manager = TreeManagerSymbols(self.tree_symbols, context_menu=self.menu_symbol, filters=self.Filters, library_manager=self.library_manager)
        self.tree_symbols_manager.AddTextColumn("name")
        self.tree_symbols_manager.OnSelectionChanged = self.onTreeModelsSelChanged
        self.tree_symbols_manager.OnItemBeforeContextMenu = self.onTreeModelsBeforeContextMenu

        # create edit symbol panel
        self.panel_edit_symbol = frames.edit_symbol_frame.EditSymbolFrame(self.splitter_horz)
        self.panel_edit_symbol.Bind( frames.edit_symbol_frame.EVT_EDIT_SYMBOL_APPLY_EVENT, self.onEditSymbolApply )
        self.panel_edit_symbol.Bind( frames.edit_symbol_frame.EVT_EDIT_SYMBOL_CANCEL_EVENT, self.onEditSymbolCancel )

        # organize panels
        self.splitter_horz.Unsplit()
        self.splitter_horz.SplitHorizontally( self.panel_up, self.panel_edit_symbol)
        self.panel_down.Hide()

        # initial state
        self.toolbar_symbol.ToggleTool(self.toggle_symbol_path.GetId(), True)
        self.Flat = False
        self.EditMode = False
#     
    @property
    def Filters(self):
        return self._filters

    @property
    def Flat(self):
        return self.tree_symbols_manager.flat
    
    @Flat.setter
    def Flat(self, value):
        self.tree_symbols_manager.flat = value
        self.tree_symbols_manager.Clear()
        self.tree_symbols_manager.Load()
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
        self.tree_symbols_manager.Load()

    def _expand_libraries(self):
        if self.Flat==False:
            for library in self.tree_symbols_manager.FindLibraries():
                self.tree_symbols_manager.Expand(library)

    def _enable(self, value):
        self.panel_up.Enabled = value


    def SetSymbol(self, symbol):
        self.panel_edit_symbol.SetSymbol(symbol)
        self._enable(True)
        
    def EditSymbol(self, symbol):
        self.EditMode = True
        self.panel_edit_symbol.EditSymbol(symbol)
        self._enable(False)

    def AddSymbol(self, library):
        self.EditMode = True
        self.panel_edit_symbol.AddSymbol(library)
        self._enable(False)

    
    def onToggleSymbolPathClicked( self, event ):
        self.Flat = not self.toolbar_symbol.GetToolState(self.toggle_symbol_path.GetId())
        event.Skip()

    def onButtonRefreshSymbolsClick( self, event ):
        self.library_manager.Reload()
        self.tree_symbols_manager.Load()

    def onFileLibChanged(self, event):
        # do a synchronize when a file change on disk
        self.tree_symbols_manager.Load()

    def onFilterChanged( self, event ):
        self.tree_symbols_manager.Load()
        self._expand_libraries()
        event.Skip()

    def onTreeModelsSelChanged( self, event ):
        item = self.tree_symbols.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_symbols_manager.ItemToObject(item)
        if isinstance(obj, Symbol)==False:
            self.panel_edit_symbol.SetSymbol(None)
            return
        self.panel_edit_symbol.SetSymbol(obj.symbol)
        event.Skip()

    def onTreeModelsBeforeContextMenu( self, event ):
        item = self.tree_symbols.GetSelection()
 
        self.menu_symbol_add.Enable(False)
        self.menu_symbol_duplicate.Enable(False)
        self.menu_symbol_remove.Enable(False)
        self.menu_symbol_edit.Enable(False)

        if item.IsOk()==False:
            return 
        obj = self.tree_symbols_manager.ItemToObject(item)

        if isinstance(obj, Symbol):
            self.menu_symbol_duplicate.Enable(True)
            self.menu_symbol_remove.Enable(True)
            self.menu_symbol_edit.Enable(True)
        else:
            self.menu_symbol_add.Enable(True)

    def onMenuSymbolAdd( self, event ):
        item = self.tree_symbols.GetSelection()
        library = None
        if item.IsOk():
            obj = self.tree_symbols_manager.ItemToObject(item)
            if isinstance(obj, Library):
                library = obj.library
            elif isinstance(obj, Symbol):
                library = obj.symbol.library
        
        if library is None:
            # TODO
            return
                
        self.AddSymbol(library)
        
        event.Skip()

    def onMenuSymbolDuplicate( self, event ):
        item = self.tree_symbols.GetSelection()
        
        event.Skip()

    def onMenuSymbolEdit( self, event ):
        item = self.tree_symbols.GetSelection()
        if not item.IsOk():
            return
        obj = self.tree_symbols_manager.ItemToObject(item)
        if isinstance(obj, Symbol)==False:
            return
        self.EditSymbol(obj.symbol)
        event.Skip()

    def onMenuSymbolRemove( self, event ):
        item = self.tree_symbols.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_symbols_manager.ItemToObject(item)
        
        symbols_to_remove = []
        library_to_remove = None
        if isinstance(obj, Library):
            library_to_remove = obj.library
            for symbol in obj.library.Symbols:
                symbols_to_remove.append(symbol)
        else:
            symbols_to_remove.append(obj.symbol)
        
        associated_parts = api.data.part.find([api.data.part.FilterSymbols(symbol.symbol_model for symbol in symbols_to_remove)])
        if len(associated_parts.all())>0:
            dlg = wx.MessageDialog(self, f"There is {len(associated_parts.all())} parts associated with selection, remove anyway?", 'Remove', wx.YES_NO | wx.ICON_EXCLAMATION)
        else:
            dlg = wx.MessageDialog(self, f"Remove selection?", 'Remove', wx.YES_NO | wx.ICON_EXCLAMATION)
        if dlg.ShowModal()==wx.ID_YES:
            try:
                if library_to_remove is None:
                    for symbol in symbols_to_remove:
                        self.library_manager.RemoveSymbol(symbol)
                else:
                    self.library_manager.RemoveLibrary(library_to_remove)
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), 'Error removing %s:'%path, wx.OK | wx.ICON_ERROR)
                dlg.Destroy()
                return

            self.library_manager.Reload()
            self.tree_symbols_manager.Load()

        dlg.Destroy()
        event.Skip()
# 
    def onEditSymbolApply( self, event ):
        self.tree_symbols_manager.Load()
        
        symbol = event.data
        symbolobj = self.tree_symbols_manager.FindSymbol(symbol)
        self.tree_symbols_manager.Select(symbolobj)

        self.SetSymbol(symbol)
        self.EditMode = False
        event.Skip()

    def onEditSymbolCancel( self, event ):
        self.tree_symbols_manager.Load()

        item = self.tree_symbols.GetSelection()
        obj = self.tree_symbols_manager.ItemToObject(item)
        if isinstance(obj, Symbol):
            self.SetSymbol(obj.symbol)
        else:
            self.SetSymbol(None)
        self.EditMode = False
        event.Skip()

    def onSearchSymbolsCancel( self, event ):
        self._filters.remove_group('search')
        event.Skip()

    def onSearchSymbolsButton( self, event ):
        self._filters.replace(FilterTextSearch(self.search_symbols.Value), 'search')
        event.Skip()

    def onSearchSymbolsTextEnter( self, event ):
        self._filters.replace(FilterTextSearch(self.search_symbols.Value), 'search')
        event.Skip()
