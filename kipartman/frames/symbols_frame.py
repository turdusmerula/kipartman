from dialogs.panel_symbols import PanelSymbols
from frames.edit_symbol_frame import EditSymbolFrame, EVT_EDIT_SYMBOL_APPLY_EVENT, EVT_EDIT_SYMBOL_CANCEL_EVENT
from kicad.kicad_file_manager import KicadFileManagerLib
from helper.filter import Filter
import rest 
import helper.tree
import os
from helper.tree import TreeImageList
from helper.exception import print_stack
from configuration import configuration
import wx
import re
import sync
import json

# help pages:
# https://wxpython.org/docs/api/wx.gizmos.TreeListCtrl-class.html

class DataModelLibraryPath(helper.tree.TreeContainerItem):
    _type_ = 1
    
    def __init__(self, path):
        super(DataModelLibraryPath, self).__init__()
        self.path = path
        
    def GetValue(self, col):
        vMap = { 
            0 : os.path.basename(self.path),
        }
        return vMap[col]

    def GetAttr(self, col, attr):
        attr.Bold = True
        return True

    def GetDragData(self):
        return {'id': self.path}

class DataModelLibrary(helper.tree.TreeContainerItem):
    _type_ = 2

    def __init__(self, path, name):
        super(DataModelLibrary, self).__init__()
        self.path = os.path.join(path, name)
        self.name = name
        
    def GetValue(self, col):
        vMap = { 
            0 : self.name,
        }
        return vMap[col]

    def GetAttr(self, col, attr):
        attr.Bold = False
        return True

    def GetDragData(self):
        return {'id': self.path}

class TreeManagerLibraries(helper.tree.TreeManager):
    def __init__(self, tree_view, *args, **kwargs):
        super(TreeManagerLibraries, self).__init__(tree_view, *args, **kwargs)

    def FindPath(self, path):
        for data in self.data:
            if isinstance(data, DataModelLibraryPath) and data.path==os.path.normpath(path):
                return data
        return None

    def FindLibrary(self, path, name):
        pathobj = self.FindPath(path)
        for data in self.data:
            if isinstance(data, DataModelLibrary) and data.name==name and data.parent==pathobj:
                return data
        return None

    def AppendPath(self, path):
        pathobj = self.FindPath(path)
        if pathobj:
            return pathobj
        pathobj = DataModelLibraryPath(path)
        parentpath = self.FindPath(os.path.dirname(path))
        self.AppendItem(parentpath, pathobj)
        return pathobj

    def AppendLibrary(self, path, name):
        libraryobj = self.FindLibrary(path, name)
        if libraryobj:
            return libraryobj
        pathobj = self.FindPath(path)
        libraryobj = DataModelLibrary(path, name)
        self.AppendItem(pathobj, libraryobj)


class DataModelSymbolPath(helper.tree.TreeContainerItem):
    _type_ = 3
    image_none = None
    
    def __init__(self, path):
        super(DataModelSymbolPath, self).__init__()
        self.path = path
        
        if not DataModelSymbolPath.image_none:
            DataModelSymbolPath.image_none = wx.Bitmap()
            DataModelSymbolPath.image_none.FromRGBA(11, 10, red=0, green=0, blue=0, alpha=0)
        
    def GetValue(self, col):
        if col==0:
            return DataModelSymbolPath.image_none
        if col==2:
            return self.path
        return ''

    def HasContainerColumns(self):
        return True

    def GetAttr(self, col, attr):
        if col==2:
            attr.Bold = True
            return True
        return False

class DataModelSymbol(helper.tree.TreeItem):
    _type_ = 4
    def __init__(self, imagelist, path, symbol):
        super(DataModelSymbol, self).__init__()
        self.imagelist = imagelist
        self.path = path
        self.symbol = symbol

    def GetValue(self, col):
        if col==0:
            return self.imagelist.GetBitmap(self.symbol.state)
        elif col==1:
            version = ''
            if self.symbol.version:
                version = str(self.symbol.version)
            return version
        elif col==2:
            if self.parent:
                name = os.path.basename(self.symbol.source_path).replace(".mod", "")
            else:
                name = os.path.join(self.path, os.path.basename(self.symbol.source_path).replace(".mod", ""))
            return name

        return None

#    def GetDragData(self):
#        if isinstance(self.parent, DataModelCategoryPath):
#            return {'id': self.symbol.id}
#        return None

class TreeManagerSymbols(helper.tree.TreeManager):
    def __init__(self, tree_view, *args, **kwargs):
        super(TreeManagerSymbols, self).__init__(tree_view, *args, **kwargs)
        self.imagelist = TreeImageList(11, 10)
                
    def FindPath(self, path):
        path = os.path.normpath(path)
        for data in self.data:
#            if isinstance(data, DataModelSymbolPath) and data.path==os.path.normpath(path):
            if isinstance(data, DataModelSymbolPath) and data.path==path:
                return data
        return None

    def FindSymbol(self, path, symbol):
        path = os.path.normpath(path)
        for data in self.data:
#            if data._type_==DataModelSymbol._type_ and data.path==path and data.symbol==symbol:
            if isinstance(data, DataModelSymbol) and data.path==os.path.normpath(path) and data.symbol==symbol:
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

    def AppendSymbol(self, path, symbol, flat=False):
        pathobj = None
        if flat==False:
            pathobj = self.FindPath(path)
        symbolobj = DataModelSymbol(self.imagelist, path, symbol)
        self.AppendItem(pathobj, symbolobj)
        return symbolobj

    def UpdateSymbol(self, path, symbol):
        symbolobj = self.FindSymbol(path, symbol)
        if symbolobj:
            self.UpdateItem(symbolobj)
        return symbolobj

    def DeleteSymbol(self, path, symbol):
        pathobj = self.FindPath(path)
        symbolobj = DataModelSymbol(self.imagelist, path, symbol)
        self.DeleteItem(pathobj, symbolobj)

class SymbolsFrameFilter(Filter):
    def __init__(self, filters_panel, onRemove):
        super(SymbolsFrameFilter, self).__init__(filters_panel, onRemove)

    def symbol_search(self, symbol, value):
        if symbol.source_path.rfind(value)>-1:
            return True
        if symbol.metadata and symbol.metadata.rfind(value)>-1:
            metadata = json.loads(symbol.metadata)
            for name in metadata:
                value = metadata[name]
                if value.rfind(value)>-1:
                    return True
        return False
    
    def FilterPath(self, path):
        if len(self.filters)==0:
            return False
        
        for filter_name in self.filters:
            filter = self.filters[filter_name]
            
            if filter['name']=='path' and path.startswith(filter['value']+os.path.sep):
                return False
                
        return True

    def FilterSymbol(self, symbol):
        if len(self.filters)==0:
            return False

        for filter_name in self.filters:
            filter = self.filters[filter_name]
            
            if filter['name']=='path' and symbol.source_path.startswith(filter['value']+os.path.sep):
                return False

            if filter['name']=='search' and self.symbol_search(symbol, filter['value']):
                return False

        return True

class SymbolsFrame(PanelSymbols): 
    def __init__(self, parent):
        super(SymbolsFrame, self).__init__(parent)
        
        self.file_manager_lib = KicadFileManagerLib()
        self.manager_lib = sync.version_manager.VersionManager(self.file_manager_lib)
        self.manager_lib.on_change_hook = self.onFileLibChanged
        
        # create libraries data
        self.tree_libraries_manager = TreeManagerLibraries(self.tree_libraries, context_menu=self.menu_libraries)
        self.tree_libraries_manager.AddTextColumn("name")
        self.tree_libraries_manager.OnSelectionChanged = self.onTreeLibrariesSelChanged
        self.tree_libraries_manager.OnItemBeforeContextMenu = self.onTreeLibrariesBeforeContextMenu

        # symbols filters
        self.symbols_filter = SymbolsFrameFilter(self.filters_panel, self.onButtonRemoveFilterClick)

        # create symbol list
        self.tree_symbols_manager = TreeManagerSymbols(self.tree_symbols, context_menu=self.menu_symbols)
        self.tree_symbols_manager.AddBitmapColumn("s")
        self.tree_symbols_manager.AddIntegerColumn("v")
        self.tree_symbols_manager.AddTextColumn("name")
        self.tree_symbols_manager.OnSelectionChanged = self.onTreeModelsSelChanged
        self.tree_symbols_manager.OnItemBeforeContextMenu = self.onTreeModelsBeforeContextMenu

        self.tree_symbols_manager.imagelist.AddFile('', 'resources/none.png')
        self.tree_symbols_manager.imagelist.AddFile(None, 'resources/none.png')
        self.tree_symbols_manager.imagelist.AddFile('conflict_add', 'resources/conflict_add.png')
        self.tree_symbols_manager.imagelist.AddFile('conflict_change', 'resources/conflict_change.png')
        self.tree_symbols_manager.imagelist.AddFile('conflict_del', 'resources/conflict_del.png')
        self.tree_symbols_manager.imagelist.AddFile('income_add', 'resources/income_add.png')
        self.tree_symbols_manager.imagelist.AddFile('income_change', 'resources/income_change.png')
        self.tree_symbols_manager.imagelist.AddFile('income_del', 'resources/income_del.png')
        self.tree_symbols_manager.imagelist.AddFile('outgo_add', 'resources/outgo_add.png')
        self.tree_symbols_manager.imagelist.AddFile('outgo_change', 'resources/outgo_change.png')
        self.tree_symbols_manager.imagelist.AddFile('outgo_del', 'resources/outgo_del.png')
        #self.tree_symbols_manager.imagelist.AddFile('prop_changed', 'resources/prop_changed.png')

        # create edit symbol panel
        self.panel_edit_symbol = EditSymbolFrame(self.symbol_splitter)
        self.symbol_splitter.SplitHorizontally(self.symbol_splitter.Window1, self.panel_edit_symbol, 400)
        self.panel_edit_symbol.Bind( EVT_EDIT_SYMBOL_APPLY_EVENT, self.onEditSymbolApply )
        self.panel_edit_symbol.Bind( EVT_EDIT_SYMBOL_CANCEL_EVENT, self.onEditSymbolCancel )

        self.toolbar_symbol.ToggleTool(self.toggle_symbol_path.GetId(), True)
        
        self.show_symbol_path = self.toolbar_symbol.GetToolState(self.toggle_symbol_path.GetId())
        self.previous_show_symbol_path = self. show_symbol_path
        
        self.show_both_changes = self.toolbar_symbol.GetToolState(self.toggle_show_both_changes.GetId())
        self.show_conflict_changes = self.toolbar_symbol.GetToolState(self.toggle_show_conflict_changes.GetId())
        self.show_incoming_changes = self.toolbar_symbol.GetToolState(self.toggle_show_incoming_changes.GetId())
        self.show_outgoing_changes = self.toolbar_symbol.GetToolState(self.toggle_show_outgoing_changes.GetId())
    
        # initial edit state
        self.show_symbol(None)
        self.edit_state = None

        self.load() 
        
    def load(self):
        try:
            self.symbols = self.manager_lib.Synchronize()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Synchronization with kipartbase failed, check your connection and try again', wx.OK | wx.ICON_ERROR)                                    
        
        self.loadLibraries()
        self.loadSymbols()
    
    def loadLibraries(self):
        
        self.tree_libraries_manager.SaveState()
        
        # load libraries tree
        for symbol_path in self.symbols:
            # decompose path
            folders = []
            library_path = os.path.dirname(symbol_path)
            path = os.path.dirname(library_path)
            library_name = os.path.basename(library_path)
            while path!='' and path!='/':
                folders.insert(0, path)
                path = os.path.dirname(path)
            
            for folder in folders:
                pathobj = self.tree_libraries_manager.FindPath(folder)
                if self.tree_libraries_manager.DropStateObject(pathobj)==False:
                    self.tree_libraries_manager.AppendPath(folder)
                    
            path = os.path.dirname(library_path)
            libraryobj = self.tree_libraries_manager.FindLibrary(path, library_name)
            if self.tree_libraries_manager.DropStateObject(libraryobj)==False:
                self.tree_libraries_manager.AppendLibrary(path, library_name)

        # add folders with no library inside
        for folder in self.file_manager_lib.folders:
            if re.compile("^.*\.lib$").match(os.path.normpath(os.path.abspath(folder))):
                path = os.path.dirname(folder)
                library_name = os.path.basename(folder)
                libraryobj = self.tree_libraries_manager.FindLibrary(path, library_name)
                if self.tree_libraries_manager.DropStateObject(libraryobj)==False:
                    self.tree_libraries_manager.AppendLibrary(path, library_name)
            else:
                pathobj = self.tree_libraries_manager.FindPath(folder)
                if self.tree_libraries_manager.DropStateObject(pathobj)==False:
                    self.tree_libraries_manager.AppendPath(folder)
            
        self.tree_libraries_manager.PurgeState()

    def loadSymbols(self):
            
        if self.previous_show_symbol_path!=self.show_symbol_path:
            # in case switch from tree to flat view 
            self.tree_symbols_manager.ClearItems()
            self.previous_show_symbol_path = self.show_symbol_path
            
        self.tree_symbols_manager.SaveState()
        
        # load symbols from local folder
        for symbol_path in self.symbols:
            library_path = os.path.dirname(symbol_path)
            if self.show_symbol_path==True:
                pathobj = self.tree_symbols_manager.FindPath(library_path)
                if self.symbols_filter.FilterPath(library_path)==False:
                    if self.tree_symbols_manager.DropStateObject(pathobj)==False:
                        self.tree_symbols_manager.AppendPath(library_path)

            symbol = self.symbols[symbol_path]
            parent = library_path

            if self.show_both_changes==False and self.show_conflict_changes==False and self.show_incoming_changes==False and self.show_outgoing_changes==False:
                show = True
            else:
                show = False
            if self.show_both_changes==True and symbol.state.rfind('outgo_')!=-1:
                show = True
            if self.show_both_changes==True and symbol.state.rfind('income_')!=-1:
                show = True
            if self.show_conflict_changes==True and symbol.state.rfind('conflict_')!=-1:
                show = True
            if self.show_incoming_changes==True and symbol.state.rfind('income_')!=-1:
                show = True
            if self.show_outgoing_changes==True and symbol.state.rfind('outgo_')!=-1:
                show = True

            libraryobj = self.tree_symbols_manager.FindSymbol(parent, symbol)
            if show==True:
                if self.symbols_filter.FilterSymbol(symbol)==False:
                    if self.tree_symbols_manager.DropStateObject(libraryobj)==False:
                        if self.show_symbol_path==True:
                            self.tree_symbols_manager.AppendSymbol(parent, symbol, flat=False)
                        else:
                            self.tree_symbols_manager.AppendSymbol(parent, symbol, flat=True)
                
        self.tree_symbols_manager.PurgeState()

    def show_symbol(self, symbol):
        # disable editing
        self.panel_edit_symbol.enable(False)
        # enable evrything else
        self.panel_path.Enabled = True
        self.panel_symbols.Enabled = True
        # set part
        self.panel_edit_symbol.SetSymbol(symbol)

    def edit_symbol(self, symbol):
        self.show_symbol(symbol)
        # enable editing
        self.panel_edit_symbol.enable(True)
        # disable evrything else
        self.panel_path.Enabled = False
        self.panel_symbols.Enabled = False
        
    def new_symbol(self, path):
        symbol = rest.model.VersionedFile()
        symbol.source_path = path         
        self.edit_symbol(symbol)

    def onFileLibChanged(self, event):
        # do a synchronize when a file change on disk
        self.load()
       
    def onTreeLibrariesSelChanged( self, event ):
        item = self.tree_libraries.GetSelection()
        if item.IsOk()==False:
            return    
        pathobj = self.tree_libraries_manager.ItemToObject(item)
        # set category filter
        self.symbols_filter.remove('path')
        if pathobj:
            self.symbols_filter.add('path', pathobj.path, pathobj.path)
        # apply new filter and reload
        self.loadSymbols()

    def onTreeLibrariesBeforeContextMenu( self, event ):
        item = self.tree_libraries.GetSelection()
        if item.IsOk()==False:
            return    
        obj = self.tree_libraries_manager.ItemToObject(item)

        self.menu_libraries_add_folder.Enable(True)
        self.menu_libraries_add_library.Enable(True)
        self.menu_libraries_add_symbol.Enable(True)
        if isinstance(obj, DataModelLibrary):
            self.menu_libraries_add_folder.Enable(False)
            self.menu_libraries_add_library.Enable(False)
        else:
            self.menu_libraries_add_symbol.Enable(False)


    def onButtonRemoveFilterClick( self, event ):
        button = event.GetEventObject()
        self.symbols_filter.remove(button.GetName())
        self.tree_libraries.UnselectAll()
        self.loadSymbols()

    def onTreeModelsSelChanged( self, event ):
        if self.edit_state:
            return
        item = self.tree_symbols.GetSelection()
        if item.IsOk()==False:
            return
        symbolobj = self.tree_symbols_manager.ItemToObject(item)
        if isinstance(symbolobj, DataModelSymbol)==False:
            self.show_symbol(None)
            return
        self.panel_edit_symbol.SetSymbol(symbolobj.symbol)

        self.show_symbol(symbolobj.symbol)

    def onTreeModelsBeforeContextMenu( self, event ):
        item = self.tree_symbols.GetSelection()
        if item.IsOk()==False:
            return    
        obj = self.tree_symbols_manager.ItemToObject(item)

        self.menu_symbols_add.Enable(True)
        self.menu_symbols_delete.Enable(True)
        self.menu_symbols_edit.Enable(True)
        if isinstance(obj, DataModelSymbol):
            self.menu_symbols_add.Enable(False)
        else:
            self.menu_symbols_delete.Enable(False)
            self.menu_symbols_edit.Enable(False)


    def onEditSymbolApply( self, event ):
        symbol = event.data
        symbol_name = event.symbol_name
                
        if self.edit_state=='add':
            # get library path
            library_path = ''
            symbol_path = os.path.join(symbol.source_path, symbol_name)
            try:
                self.manager_lib.CreateFile(symbol_path, symbol.content)
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), 'Error creating symbol', wx.OK | wx.ICON_ERROR)                                    
                return
            
        elif self.edit_state=='edit':
            # change library name if changed on disk
            library_path = os.path.dirname(symbol.source_path)
            symbol_path = os.path.normpath(os.path.join(library_path, symbol_name))
            
            if os.path.normpath(symbol.source_path)!=symbol_path:
                # file was renamed
                if self.tree_symbols.GetSelection().IsOk():
                    symbolobj = self.tree_symbols_manager.ItemToObject(self.tree_symbols.GetSelection())
                    try:
                        symbolobj.symbol = self.manager_lib.MoveFile(symbol.source_path, os.path.join(library_path, symbol_name))
                    except Exception as e:
                        print_stack()
                        wx.MessageBox(format(e), 'Error renaming symbol', wx.OK | wx.ICON_ERROR)                                    
                        return
            try:
                if symbol.content:
                    self.manager_lib.EditFile(symbol_path, symbol.content, create=True)
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), 'Error editing symbol', wx.OK | wx.ICON_ERROR)                                    
                return
            
        else:
            return
        
        self.manager_lib.EditMetadata(symbol_path, symbol.metadata)
        
        self.edit_state = None
        self.show_symbol(symbol)

        self.load()

    def onEditSymbolCancel( self, event ):
        symbol = None
        item = self.tree_symbols.GetSelection()
        if item.IsOk():
            obj = self.tree_symbols_manager.ItemToObject(item)
            if isinstance(obj, DataModelSymbol):
                symbol = obj.symbol                
        self.edit_state = None
        self.show_symbol(symbol)
    
    def onToggleSymbolPathClicked( self, event ):
        self.show_symbol_path = self.toolbar_symbol.GetToolState(self.toggle_symbol_path.GetId())
        self.load()
        
    def onToggleShowBothChangesClicked( self, event ):
        self.show_both_changes = self.toolbar_symbol.GetToolState(self.toggle_show_both_changes.GetId())
        self.load()
    
    def onToggleShowConflictChangesClicked( self, event ):
        self.show_conflict_changes = self.toolbar_symbol.GetToolState(self.toggle_show_conflict_changes.GetId())
        self.load()
    
    def onToggleShowIncomingChangesClicked( self, event ):
        self.show_incoming_changes = self.toolbar_symbol.GetToolState(self.toggle_show_incoming_changes.GetId())
        self.load()
    
    def onToggleShowOutgoingChangesClicked( self, event ):
        self.show_outgoing_changes = self.toolbar_symbol.GetToolState(self.toggle_show_outgoing_changes.GetId())
        self.load()

    def onButtonRefreshSymbolsClick( self, event ):
        self.load()
        

    def onMenuLibrariesAddFolder( self, event ):
        item = self.tree_libraries.GetSelection()
        path = ''
        if item.IsOk():
            pathobj = self.tree_libraries_manager.ItemToObject(item)
            if isinstance(pathobj, DataModelLibraryPath)==False:
                return
            path = pathobj.path

        dlg = wx.TextEntryDialog(self, 'Enter folder name', 'Add folder')
        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue()
            try:
                self.manager_lib.CreateFolder(os.path.join(path, name))
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), 'Error creating folder', wx.OK | wx.ICON_ERROR)
        dlg.Destroy()
        self.load()
        
    def onMenuLibrariesAddLibrary( self, event ):
        item = self.tree_libraries.GetSelection()
        path = ''
        if item.IsOk():
            pathobj = self.tree_libraries_manager.ItemToObject(item)
            if isinstance(pathobj, DataModelLibraryPath)==False:
                return
            path = pathobj.path

        dlg = wx.TextEntryDialog(self, 'Enter library name', 'Add library')
        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue()
            try:
                self.manager_lib.CreateFolder(os.path.join(path, name+".lib"))
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), 'Error creating library', wx.OK | wx.ICON_ERROR)
        dlg.Destroy()
        self.load()

    def onMenuLibrariesRename( self, event ):
        item = self.tree_libraries.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_libraries_manager.ItemToObject(item)
        path = obj.path 

        if isinstance(obj, DataModelLibraryPath):
            dlg = wx.TextEntryDialog(self, 'Enter new folder name', 'Rename folder')
            if dlg.ShowModal() == wx.ID_OK:
                name = dlg.GetValue()
                try:
                    newpath = os.path.join(os.path.dirname(path), name)
                    self.manager_lib.MoveFolder(path, newpath)
                except Exception as e:
                    print_stack()
                    wx.MessageBox(format(e), 'Error renaming folder', wx.OK | wx.ICON_ERROR)
            dlg.Destroy()
        elif isinstance(obj, DataModelLibrary):
            dlg = wx.TextEntryDialog(self, 'Enter new library name', 'Rename library')
            if dlg.ShowModal() == wx.ID_OK:
                name = dlg.GetValue()
                try:
                    newpath = os.path.join(os.path.dirname(path), name+".lib")
                    self.manager_lib.MoveFolder(path, newpath)
                except Exception as e:
                    print_stack()
                    wx.MessageBox(format(e), 'Error renaming library', wx.OK | wx.ICON_ERROR)
            dlg.Destroy()
        
        print "****", self.manager_lib.local_files
        self.load()
        print "++++", self.manager_lib.local_files

    def onMenuLibrariesRemove( self, event ):
        item = self.tree_libraries.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_libraries_manager.ItemToObject(item)
        path = obj.path
        try:
            self.manager_lib.DeleteFolder(path)
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Error removing %s:'%path, wx.OK | wx.ICON_ERROR)
        self.load()
        

    def onMenuLibrariesAddSymbol( self, event ):
        item = self.tree_libraries.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_libraries_manager.ItemToObject(item)
        if isinstance(obj, DataModelLibrary)==False:
            return

        self.edit_state = 'add'
        self.new_symbol(obj.path)


    def onMenuSymbolsUpdate( self, event ):
        files = []
        for item in self.tree_symbols.GetSelections():
            obj = self.tree_symbols_manager.ItemToObject(item)
            if isinstance(obj, DataModelSymbol):
                files.append(obj.symbol)
            elif isinstance(obj, DataModelSymbolPath):
                for child in obj.childs:
                    if isinstance(child, DataModelSymbol):
                        files.append(child.symbol)
        
        try:
            self.manager_lib.Update(files) 
            self.load()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Upload failed', wx.OK | wx.ICON_ERROR)
    
    def onMenuSymbolsForceUpdate( self, event ):
        files = []
        for item in self.tree_symbols.GetSelections():
            obj = self.tree_symbols_manager.ItemToObject(item)
            if isinstance(obj, DataModelSymbol):
                files.append(obj.symbol)
            elif isinstance(obj, DataModelSymbolPath):
                if obj.childs:
                    for child in obj.childs:
                        if isinstance(child, DataModelSymbol):
                            files.append(child.symbol)
        
        try:
            if len(files)>0:
                self.manager_lib.Update(files, force=True) 
            self.load()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Upload failed', wx.OK | wx.ICON_ERROR)
    
    def onMenuSymbolsCommit( self, event ):
        files = []
        for item in self.tree_symbols.GetSelections():
            obj = self.tree_symbols_manager.ItemToObject(item)
            if isinstance(obj, DataModelSymbol):
                files.append(obj.symbol)
            elif isinstance(obj, DataModelSymbolPath):
                for child in obj.childs:
                    if isinstance(child, DataModelSymbol):
                        files.append(child.symbol)
        
        try:
            print "*****", files
            self.manager_lib.Commit(files) 
            self.load()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Commit failed', wx.OK | wx.ICON_ERROR)
            
    
    def onMenuSymbolsForceCommit( self, event ):
        files = []
        for item in self.tree_symbols.GetSelections():
            obj = self.tree_symbols_manager.ItemToObject(item)
            if isinstance(obj, DataModelSymbol):
                files.append(obj.symbol)
            elif isinstance(obj, DataModelSymbolPath):
                for child in obj.childs:
                    if isinstance(child, DataModelSymbol):
                        files.append(child.symbol)
        
        try:
            self.manager_lib.Commit(files, force=True) 
            self.load()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Commit failed', wx.OK | wx.ICON_ERROR)

    def onMenuSymbolsAdd( self, event ):
        item = self.tree_symbols.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_symbols_manager.ItemToObject(item)
        if isinstance(obj, DataModelSymbolPath)==False:
            return

        self.edit_state = 'add'
        self.new_symbol(obj.path)
    
    def onMenuSymbolsEdit( self, event ):
        item = self.tree_symbols.GetSelection()
        if item.IsOk()==False:
            return
        symbolobj = self.tree_symbols_manager.ItemToObject(item)
        if isinstance(symbolobj, DataModelSymbol)==False:
            return
        state = symbolobj.symbol.state
        if state.rfind('income')!=-1 or state.rfind('conflict')!=-1:
            wx.MessageBox("Item should be updated prior to beeing edited", 'Can not edit', wx.OK | wx.ICON_ERROR)
            return
        
        self.edit_state = 'edit'
    
        self.edit_symbol(symbolobj.symbol)
    
    def onMenuSymbolsDelete( self, event ):
        files = []
        for item in self.tree_symbols.GetSelections():
            obj = self.tree_symbols_manager.ItemToObject(item)
            if isinstance(obj, DataModelSymbol):
                files.append(obj.symbol)
            elif isinstance(obj, DataModelSymbolPath):
                pass
        
        try:
            for file in files:
                self.manager_lib.DeleteFile(file) 
            self.load()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Delete failed', wx.OK | wx.ICON_ERROR)

    def onSearchSymbolsButton( self, event ):
        return self.onSearchSymbolsTextEnter(event)
    
    def onSearchSymbolsTextEnter( self, event ):
        # set search filter
        self.symbols_filter.remove('search')
        if self.search_symbols.Value!='':
            self.symbols_filter.add('search', self.search_symbols.Value)
        # apply new filter and reload
        self.loadSymbols()
