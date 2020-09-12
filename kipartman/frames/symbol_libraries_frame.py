from dialogs.panel_symbol_libraries import PanelSymbolLibraries
# from frames.edit_symbol_frame import EditSymbolFrame, EVT_EDIT_SYMBOL_APPLY_EVENT, EVT_EDIT_SYMBOL_CANCEL_EVENT
from kicad.kicad_file_manager_symbols import KicadLibraryManager
import kicad.kicad_file_manager
import helper.tree
import os
import api.data.library
import wx
from helper.exception import print_stack
from helper.log import log
import kicad

state_image_list = None

class LibraryPath(helper.tree.TreeContainerItem):
    def __init__(self, path):
        super(LibraryPath, self).__init__()
        self.path = path
    
    @property
    def Path(self):
        return self.path
    
    def GetValue(self, col):
#         if col==0:
#             global state_image_list
#             return state_image_list.GetBitmap('')
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
#         if col==0:
#             return state_image_list.GetBitmap('')
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
        
        # reload libraries from disk
#         self.library_manager.Load()

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

class SymbolLibrariesFrame(PanelSymbolLibraries): 
    def __init__(self, *args, **kwargs):
        super(SymbolLibrariesFrame, self).__init__(*args, **kwargs)

        # react to file change 
        self.library_manager = KicadLibraryManager(self)
        self.Bind( kicad.kicad_file_manager.EVT_FILE_CHANGED, self.onFileLibChanged )

        # create libraries data
        self.tree_libraries_manager = TreeManagerLibraries(self.tree_libraries, context_menu=self.menu_libraries, library_manager=self.library_manager)
#         self.tree_libraries_manager.AddBitmapColumn("s")
        self.tree_libraries_manager.AddTextColumn("name")
        self.tree_libraries_manager.OnSelectionChanged = self.onTreeLibrariesSelChanged
        self.tree_libraries_manager.OnItemBeforeContextMenu = self.onTreeLibrariesBeforeContextMenu

        global state_image_list
        state_image_list = helper.tree.TreeImageList(11, 10)
        state_image_list.AddFile('', 'resources/none.png')
        state_image_list.AddFile(None, 'resources/none.png')
        state_image_list.AddFile('conflict_add', 'resources/conflict_add.png')
        state_image_list.AddFile('conflict_change', 'resources/conflict_change.png')
        state_image_list.AddFile('conflict_del', 'resources/conflict_del.png')
        state_image_list.AddFile('income_add', 'resources/income_add.png')
        state_image_list.AddFile('income_change', 'resources/income_change.png')
        state_image_list.AddFile('income_del', 'resources/income_del.png')
        state_image_list.AddFile('outgo_add', 'resources/outgo_add.png')
        state_image_list.AddFile('outgo_change', 'resources/outgo_change.png')
        state_image_list.AddFile('outgo_del', 'resources/outgo_del.png')
        #state_image_list.AddFile('prop_changed', 'resources/prop_changed.png')
#     
    def activate(self):
        self.tree_libraries_manager.Load()

    def onFileLibChanged(self, event):
        print("----", self, event.path)
        # do a synchronize when a file change on disk
        self.tree_libraries_manager.Load()

    def onButtonRefreshCategoriesClick( self, event ):
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
                library_manager.CreateFolder(os.path.join(path, name))
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), 'Error creating folder', wx.OK | wx.ICON_ERROR)
                dlg.Destroy()
                return

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
                library = library_manager.CreateLibrary(os.path.join(path, name+".lib"))
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), 'Error creating library', wx.OK | wx.ICON_ERROR)
                dlg.Destroy()
                return
            
            # save library on disk
            library.Save()
            
            # save library on database
            # TODO
            
            self.tree_libraries_manager.Load()
            
            # select created item
            libraryobj = self.tree_libraries_manager.FindLibrary(library.Path)
            if libraryobj is not None:
                self.tree_libraries_manager.Select(libraryobj)
        dlg.Destroy()
        
        event.Skip()

    def onMenuLibrariesRename( self, event ):
        event.Skip()

    def onMenuLibrariesRemove( self, event ):
        event.Skip()

    def onMenuLibrariesAddSymbol( self, event ):
        event.Skip()

    def onTreeLibrariesBeforeContextMenu( self, event ):
        item = self.tree_libraries.GetSelection()
        if item.IsOk()==False:
            return    
        obj = self.tree_libraries_manager.ItemToObject(item)

        self.menu_libraries_add_folder.Enable(True)
        self.menu_libraries_add_library.Enable(True)
        self.menu_libraries_add_symbol.Enable(True)
        if isinstance(obj, Library)==False:
            self.menu_libraries_add_symbol.Enable(False)

        event.Skip()

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
