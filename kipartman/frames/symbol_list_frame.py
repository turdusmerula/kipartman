from dialogs.panel_symbol_list import PanelSymbolList
import frames.edit_symbol_frame
import os
import helper.tree
import helper.filter
from kicad.kicad_file_manager_symbols import KicadLibraryManager
import kicad.kicad_file_manager
import api.data.library
import api.data.library_symbol
from helper.log import log

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
#         self.library_manager.Load()

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
 
class FilterLibraryPath(api.data.library_symbol.FilterPath):
    def __init__(self, path):
        super(FilterLibraryPath, self).__init__(path)
    
    def apply(self, request):
        if isinstance(request, kicad.kicad_file_manager_symbols.KicadLibrary):
            return request.Path.startswith(self.path)==False
        else:
            return super(FilterLibraryPath, self).apply(request)
    
class SymbolListFrame(PanelSymbolList): 
    def __init__(self, *args, **kwargs):
        super(SymbolListFrame, self).__init__(*args, **kwargs)

        # react to file change
        self.library_manager = KicadLibraryManager(self)
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

    def activate(self):
        self.tree_symbols_manager.Load()

    def _expand_libraries(self):
        if self.Flat==False:
            for library in self.tree_symbols_manager.FindLibraries():
                self.tree_symbols_manager.Expand(library)
    
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

#     def onTreeLibrariesSelChanged( self, event ):
#         item = self.tree_libraries.GetSelection()
#         if item.IsOk()==False:
#             return    
#         pathobj = self.tree_libraries_manager.ItemToObject(item)
#         # set category filter
#         self.symbols_filter.remove('path')
#         if pathobj:
#             self.symbols_filter.add('path', pathobj.path, pathobj.path)
#         # apply new filter and reload
#         self.loadSymbols()
# 
#     def onButtonRemoveFilterClick( self, event ):
#         button = event.GetEventObject()
#         self.symbols_filter.remove(button.GetName())
#         self.tree_libraries.UnselectAll()
#         self.loadSymbols()
# 
# 
# 
# 
    def onEditSymbolApply( self, event ):
        pass
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
        pass
#         symbol = None
#         item = self.tree_symbols.GetSelection()
#         if item.IsOk():
#             obj = self.tree_symbols_manager.ItemToObject(item)
#             if isinstance(obj, DataModelSymbol):
#                 symbol = obj.symbol                
#         self.edit_state = None
#         self.show_symbol(symbol)
#     
#         
#     def onToggleShowBothChangesClicked( self, event ):
#         self.show_both_changes = self.toolbar_symbol.GetToolState(self.toggle_show_both_changes.GetId())
#         self.load()
#     
#     def onToggleShowConflictChangesClicked( self, event ):
#         self.show_conflict_changes = self.toolbar_symbol.GetToolState(self.toggle_show_conflict_changes.GetId())
#         self.load()
#     
#     def onToggleShowIncomingChangesClicked( self, event ):
#         self.show_incoming_changes = self.toolbar_symbol.GetToolState(self.toggle_show_incoming_changes.GetId())
#         self.load()
#     
#     def onToggleShowOutgoingChangesClicked( self, event ):
#         self.show_outgoing_changes = self.toolbar_symbol.GetToolState(self.toggle_show_outgoing_changes.GetId())
#         self.load()
# 
#         
# 
#     def onMenuLibrariesAddFolder( self, event ):
#         item = self.tree_libraries.GetSelection()
#         path = ''
#         if item.IsOk():
#             pathobj = self.tree_libraries_manager.ItemToObject(item)
#             if isinstance(pathobj, DataModelLibraryPath)==False:
#                 return
#             path = pathobj.path
# 
#         dlg = wx.TextEntryDialog(self, 'Enter folder name', 'Add folder')
#         if dlg.ShowModal() == wx.ID_OK:
#             name = dlg.GetValue()
#             try:
#                 self.manager_lib.CreateFolder(os.path.join(path, name))
#             except Exception as e:
#                 print_stack()
#                 wx.MessageBox(format(e), 'Error creating folder', wx.OK | wx.ICON_ERROR)
#         dlg.Destroy()
#         self.load()
#         
#     def onMenuLibrariesAddLibrary( self, event ):
#         item = self.tree_libraries.GetSelection()
#         path = ''
#         if item.IsOk():
#             pathobj = self.tree_libraries_manager.ItemToObject(item)
#             if isinstance(pathobj, DataModelLibraryPath)==False:
#                 return
#             path = pathobj.path
# 
#         dlg = wx.TextEntryDialog(self, 'Enter library name', 'Add library')
#         if dlg.ShowModal() == wx.ID_OK:
#             name = dlg.GetValue()
#             try:
#                 self.manager_lib.CreateFolder(os.path.join(path, name+".lib"))
#             except Exception as e:
#                 print_stack()
#                 wx.MessageBox(format(e), 'Error creating library', wx.OK | wx.ICON_ERROR)
#         dlg.Destroy()
#         self.load()
# 
#     def onMenuLibrariesRename( self, event ):
#         item = self.tree_libraries.GetSelection()
#         if item.IsOk()==False:
#             return
#         obj = self.tree_libraries_manager.ItemToObject(item)
#         path = obj.path 
# 
#         if isinstance(obj, DataModelLibraryPath):
#             dlg = wx.TextEntryDialog(self, 'Enter new folder name', 'Rename folder')
#             if dlg.ShowModal() == wx.ID_OK:
#                 name = dlg.GetValue()
#                 try:
#                     newpath = os.path.join(os.path.dirname(path), name)
#                     self.manager_lib.MoveFolder(path, newpath)
#                 except Exception as e:
#                     print_stack()
#                     wx.MessageBox(format(e), 'Error renaming folder', wx.OK | wx.ICON_ERROR)
#             dlg.Destroy()
#         elif isinstance(obj, DataModelLibrary):
#             dlg = wx.TextEntryDialog(self, 'Enter new library name', 'Rename library')
#             if dlg.ShowModal() == wx.ID_OK:
#                 name = dlg.GetValue()
#                 try:
#                     newpath = os.path.join(os.path.dirname(path), name+".lib")
#                     self.manager_lib.MoveFolder(path, newpath)
#                 except Exception as e:
#                     print_stack()
#                     wx.MessageBox(format(e), 'Error renaming library', wx.OK | wx.ICON_ERROR)
#             dlg.Destroy()
#         
#         self.load()
# 
#     def onMenuLibrariesRemove( self, event ):
#         item = self.tree_libraries.GetSelection()
#         if item.IsOk()==False:
#             return
#         obj = self.tree_libraries_manager.ItemToObject(item)
#         path = obj.path
#         try:
#             self.manager_lib.DeleteFolder(path)
#         except Exception as e:
#             print_stack()
#             wx.MessageBox(format(e), 'Error removing %s:'%path, wx.OK | wx.ICON_ERROR)
#         self.load()
#         
# 
#     def onMenuLibrariesAddSymbol( self, event ):
#         item = self.tree_libraries.GetSelection()
#         if item.IsOk()==False:
#             return
#         obj = self.tree_libraries_manager.ItemToObject(item)
#         if isinstance(obj, DataModelLibrary)==False:
#             return
# 
#         self.edit_state = 'add'
#         self.new_symbol(obj.path)
# 
# 
#     def onMenuSymbolsUpdate( self, event ):
#         files = []
#         for item in self.tree_symbols.GetSelections():
#             obj = self.tree_symbols_manager.ItemToObject(item)
#             if isinstance(obj, DataModelSymbol):
#                 files.append(obj.symbol)
#             elif isinstance(obj, DataModelSymbolPath):
#                 for child in obj.childs:
#                     if isinstance(child, DataModelSymbol):
#                         files.append(child.symbol)
#         
#         try:
#             self.manager_lib.Update(files) 
#             self.load()
#         except Exception as e:
#             print_stack()
#             wx.MessageBox(format(e), 'Upload failed', wx.OK | wx.ICON_ERROR)
#     
#     def onMenuSymbolsForceUpdate( self, event ):
#         files = []
#         for item in self.tree_symbols.GetSelections():
#             obj = self.tree_symbols_manager.ItemToObject(item)
#             if isinstance(obj, DataModelSymbol):
#                 files.append(obj.symbol)
#             elif isinstance(obj, DataModelSymbolPath):
#                 if obj.childs:
#                     for child in obj.childs:
#                         if isinstance(child, DataModelSymbol):
#                             files.append(child.symbol)
#         
#         try:
#             if len(files)>0:
#                 self.manager_lib.Update(files, force=True) 
#             self.load()
#         except Exception as e:
#             print_stack()
#             wx.MessageBox(format(e), 'Upload failed', wx.OK | wx.ICON_ERROR)
#     
#     def onMenuSymbolsCommit( self, event ):
#         files = []
#         for item in self.tree_symbols.GetSelections():
#             obj = self.tree_symbols_manager.ItemToObject(item)
#             if isinstance(obj, DataModelSymbol):
#                 files.append(obj.symbol)
#             elif isinstance(obj, DataModelSymbolPath):
#                 for child in obj.childs:
#                     if isinstance(child, DataModelSymbol):
#                         files.append(child.symbol)
#         
#         try:
#             self.manager_lib.Commit(files) 
#             self.load()
#         except Exception as e:
#             print_stack()
#             wx.MessageBox(format(e), 'Commit failed', wx.OK | wx.ICON_ERROR)
#             
#     
#     def onMenuSymbolsForceCommit( self, event ):
#         files = []
#         for item in self.tree_symbols.GetSelections():
#             obj = self.tree_symbols_manager.ItemToObject(item)
#             if isinstance(obj, DataModelSymbol):
#                 files.append(obj.symbol)
#             elif isinstance(obj, DataModelSymbolPath):
#                 for child in obj.childs:
#                     if isinstance(child, DataModelSymbol):
#                         files.append(child.symbol)
#         
#         try:
#             self.manager_lib.Commit(files, force=True) 
#             self.load()
#         except Exception as e:
#             print_stack()
#             wx.MessageBox(format(e), 'Commit failed', wx.OK | wx.ICON_ERROR)
# 
#     def onMenuSymbolsAdd( self, event ):
#         item = self.tree_symbols.GetSelection()
#         if item.IsOk()==False:
#             return
#         obj = self.tree_symbols_manager.ItemToObject(item)
#         if isinstance(obj, DataModelSymbolPath)==False:
#             return
# 
#         self.edit_state = 'add'
#         self.new_symbol(obj.path)
#     
#     def onMenuSymbolsEdit( self, event ):
#         item = self.tree_symbols.GetSelection()
#         if item.IsOk()==False:
#             return
#         symbolobj = self.tree_symbols_manager.ItemToObject(item)
#         if isinstance(symbolobj, DataModelSymbol)==False:
#             return
#         state = symbolobj.symbol.state
#         if state.rfind('income')!=-1 or state.rfind('conflict')!=-1:
#             wx.MessageBox("Item should be updated prior to beeing edited", 'Can not edit', wx.OK | wx.ICON_ERROR)
#             return
#         
#         self.edit_state = 'edit'
#     
#         self.edit_symbol(symbolobj.symbol)
#     
#     def onMenuSymbolsDelete( self, event ):
#         files = []
#         for item in self.tree_symbols.GetSelections():
#             obj = self.tree_symbols_manager.ItemToObject(item)
#             if isinstance(obj, DataModelSymbol):
#                 files.append(obj.symbol)
#             elif isinstance(obj, DataModelSymbolPath):
#                 pass
#         
#         try:
#             for file in files:
#                 self.manager_lib.DeleteFile(file) 
#             self.load()
#         except Exception as e:
#             print_stack()
#             wx.MessageBox(format(e), 'Delete failed', wx.OK | wx.ICON_ERROR)
# 
#     def onSearchSymbolsButton( self, event ):
#         return self.onSearchSymbolsTextEnter(event)
#     
#     def onSearchSymbolsTextEnter( self, event ):
#         # set search filter
#         self.symbols_filter.remove('search')
#         if self.search_symbols.Value!='':
#             self.symbols_filter.add('search', self.search_symbols.Value)
#         # apply new filter and reload
#         self.loadSymbols()
