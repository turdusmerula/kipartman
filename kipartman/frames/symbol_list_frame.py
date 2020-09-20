from dialogs.panel_symbol_list import PanelSymbolList
import frames.edit_symbol_frame
import os
import helper.tree
import helper.filter
from kicad.kicad_file_manager_symbols import KicadSymbolLibraryManager, KicadSymbolFile, KicadSymbol
import kicad.kicad_file_manager
import api.data.kicad_symbol_library
import api.data.kicad_symbol
from helper.log import log
from builtins import isinstance
import wx

# from dialogs.panel_symbols import PanelSymbols
# from frames.edit_symbol_frame import EditSymbolFrame, EVT_EDIT_SYMBOL_APPLY_EVENT, EVT_EDIT_SYMBOL_CANCEL_EVENT
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
            for symbol in library.Symbols:
                symbolobj = self.FindSymbol(symbol)
                if symbolobj is None:
                    symbolobj = self.AppendSymbol(None, symbol)
                else:
                    symbolobj.symbol = symbol
                    self.Update(symbolobj)
    
    def LoadTree(self):
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
 
class FilterLibraryPath(api.data.kicad_symbol_library.FilterPath):
    def __init__(self, path):
        super(FilterLibraryPath, self).__init__(path)
    
    def apply(self, request):
        if isinstance(request, kicad.kicad_file_manager_symbols.KicadLibrary):
            return request.Path.startswith(self.path)==False
        else:
            return super(FilterLibraryPath, self).apply(request)

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
        self.tree_symbols_manager = TreeManagerSymbols(self.tree_symbols, context_menu=self.menu_symbols, filters=self.Filters, library_manager=self.library_manager)
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
    
    
    def onFileLibChanged(self, event):
        # do a synchronize when a file change on disk
        self.tree_symbols_manager.Load()

    def onButtonRefreshSymbolsClick( self, event ):
        self.library_manager.Reload()
        self.tree_symbols_manager.Load()

    def onTreeModelsBeforeContextMenu( self, event ):
        item = self.tree_symbols.GetSelection()
        if item.IsOk()==False:
            return    
        obj = self.tree_symbols_manager.ItemToObject(item)
 
        self.menu_symbols_add.Enable(True)
        self.menu_symbols_delete.Enable(True)
        self.menu_symbols_edit.Enable(True)
        if isinstance(obj, Symbol):
            self.menu_symbols_add.Enable(False)
        else:
            self.menu_symbols_delete.Enable(False)
            self.menu_symbols_edit.Enable(False)

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

    def onToggleSymbolPathClicked( self, event ):
        self.Flat = not self.toolbar_symbol.GetToolState(self.toggle_symbol_path.GetId())
        event.Skip()

    def onFilterChanged( self, event ):
        self.tree_symbols_manager.Load()
        self._expand_libraries()
        event.Skip()

    def onMenuSymbolsAdd( self, event ):
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
        
        symbol_file = KicadSymbolFile(library.library_file, "", "")
        symbol = KicadSymbol(library, symbol_file=symbol_file)
        
        self.EditSymbol(symbol)
        
        event.Skip()

    def onMenuSymbolsEdit( self, event ):
        event.Skip()

    def onMenuSymbolsDelete( self, event ):
        event.Skip()
# 
    def onEditSymbolApply( self, event ):
        pass

    def onSearchSymbolsCancel( self, event ):
        event.Skip()

    def onSearchSymbolsButton( self, event ):
        event.Skip()

    def onSearchSymbolsTextEnter( self, event ):
        event.Skip()

#         symbol = event.data
#         symbol_name = event.symbol_name
#                 
#         if self.edit_state=='add':
#             # get library path
#             library_path = ''
#             symbol_path = os.path.join(symbol.source_path, symbol_name)
#             try:
#                 self.manager_lib.CreateFile(symbol_path, symbol.content)
#             except Exception as e:
#                 print_stack()
#                 wx.MessageBox(format(e), 'Error creating symbol', wx.OK | wx.ICON_ERROR)                                    
#                 return
#             
#         elif self.edit_state=='edit':
#             # change library name if changed on disk
#             library_path = os.path.dirname(symbol.source_path)
#             symbol_path = os.path.normpath(os.path.join(library_path, symbol_name))
#             
#             if os.path.normpath(symbol.source_path)!=symbol_path:
#                 # file was renamed
#                 if self.tree_symbols.GetSelection().IsOk():
#                     symbolobj = self.tree_symbols_manager.ItemToObject(self.tree_symbols.GetSelection())
#                     try:
#                         symbolobj.symbol = self.manager_lib.MoveFile(symbol.source_path, os.path.join(library_path, symbol_name))
#                     except Exception as e:
#                         print_stack()
#                         wx.MessageBox(format(e), 'Error renaming symbol', wx.OK | wx.ICON_ERROR)                                    
#                         return
#             try:
#                 if symbol.content:
#                     self.manager_lib.EditFile(symbol_path, symbol.content, create=True)
#             except Exception as e:
#                 print_stack()
#                 wx.MessageBox(format(e), 'Error editing symbol', wx.OK | wx.ICON_ERROR)                                    
#                 return
#             
#         else:
#             return
#         
#         self.manager_lib.EditMetadata(symbol_path, symbol.metadata)
#         
#         self.edit_state = None
#         self.show_symbol(symbol)
# 
#         self.load()
# 
    def onEditSymbolCancel( self, event ):
        self.tree_symbols_manager.Load()
        
        # reload the part after changing it
        item = self.tree_symbols.GetSelection()
        obj = self.tree_symbols_manager.ItemToObject(item)
        if isinstance(obj, Symbol):
            self.SetSymbol(obj.symbol)
        else:
            self.SetSymbol(None)

        self.EditMode = False        
        event.Skip()
