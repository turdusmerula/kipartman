from dialogs.panel_modules import PanelModules
from frames.edit_module_frame import EditModuleFrame, EVT_EDIT_FOOTPRINT_APPLY_EVENT, EVT_EDIT_FOOTPRINT_CANCEL_EVENT
from kicad.kicad_file_manager import KicadFileManagerModule
from helper.filter import Filter
import rest
import helper.tree
import os
from helper.tree import TreeImageList
from helper.exception import print_stack
import wx
import re
import sync.version_manager
import json

# help pages:
# https://wxpython.org/docs/api/wx.gizmos.TreeListCtrl-class.html

class DataModelLibraryPath(helper.tree.TreeContainerItem):
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


class DataModelModulePath(helper.tree.TreeContainerItem):
    image_none = None
    
    def __init__(self, path):
        super(DataModelModulePath, self).__init__()
        self.path = path
        
        if not DataModelModulePath.image_none:
            DataModelModulePath.image_none = wx.Bitmap()
            DataModelModulePath.image_none.FromRGBA(11, 10, red=0, green=0, blue=0, alpha=0)
        
    def GetValue(self, col):
        if col==0:
            return DataModelModulePath.image_none
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

class DataModelModule(helper.tree.TreeItem):
    def __init__(self, imagelist, path, module):
        super(DataModelModule, self).__init__()
        self.imagelist = imagelist
        self.path = path
        self.module = module

    def GetValue(self, col):
        version = ''
        if self.module.version:
            version = str(self.module.version)
        if self.parent:
            name = os.path.basename(self.module.source_path).replace(".kicad_mod", "")
        else:
            name = os.path.join(self.path, os.path.basename(self.module.source_path).replace(".kicad_mod", ""))
        vMap = {
            0 : self.imagelist.GetBitmap(self.module.state), 
            1 : str(version),
            2 : name,
        }
#        return wx.dataview.DataViewIconText(vMap[col], None)
        return vMap[col]

#    def GetDragData(self):
#        if isinstance(self.parent, DataModelCategoryPath):
#            return {'id': self.module.id}
#        return None

class TreeManagerModules(helper.tree.TreeManager):
    def __init__(self, tree_view, *args, **kwargs):
        super(TreeManagerModules, self).__init__(tree_view, *args, **kwargs)
        self.imagelist = TreeImageList(11, 10)
                
    def FindPath(self, path):
        for data in self.data:
            if isinstance(data, DataModelModulePath) and data.path==os.path.normpath(path):
                return data
        return None

    def FindModule(self, path, module):
        for data in self.data:
            if isinstance(data, DataModelModule) and data.path==os.path.normpath(path) and data.module==module:
                return data
        return None

    def AppendPath(self, path):
        pathobj = self.FindPath(path)
        if pathobj:
            return pathobj
        pathobj = DataModelModulePath(path)
        parentpath = self.FindPath(os.path.dirname(path))
        self.AppendItem(parentpath, pathobj)
        return pathobj

    def AppendModule(self, path, module, flat=False):
        pathobj = None
        if flat==False:
            pathobj = self.FindPath(path)
        moduleobj = DataModelModule(self.imagelist, path, module)
        self.AppendItem(pathobj, moduleobj)
        return moduleobj

    def UpdateModule(self, path, module):
        moduleobj = self.FindModule(path, module)
        if moduleobj:
            self.UpdateItem(moduleobj)
        return moduleobj

    def DeleteModule(self, path, module):
        pathobj = self.FindPath(path)
        moduleobj = DataModelModule(self.imagelist, path, module)
        self.DeleteItem(pathobj, moduleobj)

class ModulesFrameFilter(Filter):
    def __init__(self, filters_panel, onRemove):
        super(ModulesFrameFilter, self).__init__(filters_panel, onRemove)

    def module_search(self, module, value):
        if module.source_path.rfind(value)>-1:
            return True
        if module.metadata and module.metadata.rfind(value)>-1:
            metadata = json.loads(module.metadata)
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

    def FilterModule(self, module):
        if len(self.filters)==0:
            return False

        for filter_name in self.filters:
            filter = self.filters[filter_name]
            
            if filter['name']=='path' and module.source_path.startswith(filter['value']+os.path.sep):
                return False

            if filter['name']=='search' and self.module_search(module, filter['value']):
                return False

        return True

class ModulesFrame(PanelModules): 
    def __init__(self, parent):
        super(ModulesFrame, self).__init__(parent)
        
        self.file_manager_module = KicadFileManagerModule()
        self.manager_module = sync.version_manager.VersionManager(self.file_manager_module)
        self.manager_module.on_change_hook = self.onFileModuleChanged
        
        # create libraries data
        self.tree_libraries_manager = TreeManagerLibraries(self.tree_libraries, context_menu=self.menu_libraries)
        self.tree_libraries_manager.AddTextColumn("name")
        self.tree_libraries_manager.OnSelectionChanged = self.onTreeLibrariesSelChanged
        self.tree_libraries_manager.OnItemBeforeContextMenu = self.onTreeLibrariesBeforeContextMenu

        # modules filters
        self.modules_filter = ModulesFrameFilter(self.filters_panel, self.onButtonRemoveFilterClick)

        # create module list
        self.tree_modules_manager = TreeManagerModules(self.tree_modules, context_menu=self.menu_modules)
        self.tree_modules_manager.AddBitmapColumn("s")
        self.tree_modules_manager.AddIntegerColumn("v")
        self.tree_modules_manager.AddTextColumn("name")
        self.tree_modules_manager.OnSelectionChanged = self.onTreeModulesSelChanged
        self.tree_modules_manager.OnItemBeforeContextMenu = self.onTreeModulesBeforeContextMenu

        self.tree_modules_manager.imagelist.AddFile('', 'resources/none.png')
        self.tree_modules_manager.imagelist.AddFile(None, 'resources/none.png')
        self.tree_modules_manager.imagelist.AddFile('conflict_add', 'resources/conflict_add.png')
        self.tree_modules_manager.imagelist.AddFile('conflict_change', 'resources/conflict_change.png')
        self.tree_modules_manager.imagelist.AddFile('conflict_del', 'resources/conflict_del.png')
        self.tree_modules_manager.imagelist.AddFile('income_add', 'resources/income_add.png')
        self.tree_modules_manager.imagelist.AddFile('income_change', 'resources/income_change.png')
        self.tree_modules_manager.imagelist.AddFile('income_del', 'resources/income_del.png')
        self.tree_modules_manager.imagelist.AddFile('outgo_add', 'resources/outgo_add.png')
        self.tree_modules_manager.imagelist.AddFile('outgo_change', 'resources/outgo_change.png')
        self.tree_modules_manager.imagelist.AddFile('outgo_del', 'resources/outgo_del.png')
        #self.tree_modules_manager.imagelist.AddFile('prop_changed', 'resources/prop_changed.png')

        # create edit module panel
        self.panel_edit_module = EditModuleFrame(self.module_splitter)
        self.module_splitter.SplitHorizontally(self.module_splitter.Window1, self.panel_edit_module, 400)
        self.panel_edit_module.Bind( EVT_EDIT_FOOTPRINT_APPLY_EVENT, self.onEditModuleApply )
        self.panel_edit_module.Bind( EVT_EDIT_FOOTPRINT_CANCEL_EVENT, self.onEditModuleCancel )

        self.toolbar_module.ToggleTool(self.toggle_module_path.GetId(), True)
        
        self.show_module_path = self.toolbar_module.GetToolState(self.toggle_module_path.GetId())
        self.previous_show_module_path = self. show_module_path
        
        self.show_both_changes = self.toolbar_module.GetToolState(self.toggle_show_both_changes.GetId())
        self.show_conflict_changes = self.toolbar_module.GetToolState(self.toggle_show_conflict_changes.GetId())
        self.show_incoming_changes = self.toolbar_module.GetToolState(self.toggle_show_incoming_changes.GetId())
        self.show_outgoing_changes = self.toolbar_module.GetToolState(self.toggle_show_outgoing_changes.GetId())
    
        # initial edit state
        self.show_module(None)
        self.edit_state = None

        self.load() 
        
    def load(self):
        try:
            self.modules = self.manager_module.Synchronize()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Synchronization with kipartbase failed, check your connection and try again', wx.OK | wx.ICON_ERROR)                                    
            
        #self.modules = self.manager_module.
        #self.modules =  self.resource_module.Synchronize()
        
        self.loadLibraries()
        self.loadModules()
    
    def loadLibraries(self):
        
        self.tree_libraries_manager.SaveState()
        
        # load libraries tree
        for module_path in self.modules:
            # decompose path
            folders = []
            library_path = os.path.dirname(module_path)
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
        for folder in self.file_manager_module.folders:
            if re.compile("^.*\.module$").match(os.path.normpath(os.path.abspath(folder))):
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

    def loadModules(self):
            
        if self.previous_show_module_path!=self.show_module_path:
            # in case switch from tree to flat view 
            self.tree_modules_manager.ClearItems()
            self.previous_show_module_path = self.show_module_path
            
        self.tree_modules_manager.SaveState()
        
        # load modules from local folder
        for module_path in self.modules:
            library_path = os.path.dirname(module_path)
            if self.show_module_path==True:
                pathobj = self.tree_modules_manager.FindPath(library_path)
                if self.modules_filter.FilterPath(library_path)==False:
                    if self.tree_modules_manager.DropStateObject(pathobj)==False:
                        self.tree_modules_manager.AppendPath(library_path)

            module = self.modules[module_path]
            parent = library_path

            if self.show_both_changes==False and self.show_conflict_changes==False and self.show_incoming_changes==False and self.show_outgoing_changes==False:
                show = True
            else:
                show = False
            if self.show_both_changes==True and module.state.rfind('outgo_')!=-1:
                show = True
            if self.show_both_changes==True and module.state.rfind('income_')!=-1:
                show = True
            if self.show_conflict_changes==True and module.state.rfind('conflict_')!=-1:
                show = True
            if self.show_incoming_changes==True and module.state.rfind('income_')!=-1:
                show = True
            if self.show_outgoing_changes==True and module.state.rfind('outgo_')!=-1:
                show = True

            libraryobj = self.tree_modules_manager.FindModule(parent, module)
            if show==True:
                if self.modules_filter.FilterModule(module)==False:
                    if self.tree_modules_manager.DropStateObject(libraryobj)==False:
                        if self.show_module_path==True:
                            self.tree_modules_manager.AppendModule(parent, module, flat=False)
                        else:
                            self.tree_modules_manager.AppendModule(parent, module, flat=True)
                
        self.tree_modules_manager.PurgeState()

    def show_module(self, module):
        # disable editing
        self.panel_edit_module.enable(False)
        # enable evrything else
        self.panel_path.Enabled = True
        self.panel_modules.Enabled = True
        # set part
        self.panel_edit_module.SetModule(module)

    def edit_module(self, module):
        self.show_module(module)
        # enable editing
        self.panel_edit_module.enable(True)
        # disable evrything else
        self.panel_path.Enabled = False
        self.panel_modules.Enabled = False
        
    def new_module(self, path):
        module = rest.model.VersionedFile()
        module.source_path = path         
        self.edit_module(module)

    def onFileModuleChanged(self, event):
        # do a synchronize when a file change on disk
        self.load()
       
    def onTreeLibrariesSelChanged( self, event ):
        item = self.tree_libraries.GetSelection()
        if item.IsOk()==False:
            return    
        pathobj = self.tree_libraries_manager.ItemToObject(item)
        # set category filter
        self.modules_filter.remove('path')
        if pathobj:
            self.modules_filter.add('path', pathobj.path, pathobj.path)
        # apply new filter and reload
        self.loadModules()

    def onTreeLibrariesBeforeContextMenu( self, event ):
        item = self.tree_libraries.GetSelection()
        if item.IsOk()==False:
            return    
        obj = self.tree_libraries_manager.ItemToObject(item)

        self.menu_libraries_add_folder.Enable(True)
        self.menu_libraries_add_library.Enable(True)
        self.menu_libraries_add_module.Enable(True)
        if isinstance(obj, DataModelLibrary):
            self.menu_libraries_add_folder.Enable(False)
            self.menu_libraries_add_library.Enable(False)
        else:
            self.menu_libraries_add_module.Enable(False)


    def onButtonRemoveFilterClick( self, event ):
        button = event.GetEventObject()
        self.modules_filter.remove(button.GetName())
        self.tree_libraries.UnselectAll()
        self.loadModules()

    def onTreeModulesSelChanged( self, event ):
        if self.edit_state:
            return
        item = self.tree_modules.GetSelection()
        if item.IsOk()==False:
            return
        moduleobj = self.tree_modules_manager.ItemToObject(item)
        if isinstance(moduleobj, DataModelModule)==False:
            self.show_module(None)
            return
        self.panel_edit_module.SetModule(moduleobj.module)

        self.show_module(moduleobj.module)

    def onTreeModulesBeforeContextMenu( self, event ):
        item = self.tree_modules.GetSelection()
        if item.IsOk()==False:
            return    
        obj = self.tree_modules_manager.ItemToObject(item)

        self.menu_modules_add.Enable(True)
        self.menu_modules_delete.Enable(True)
        self.menu_modules_edit.Enable(True)
        if isinstance(obj, DataModelModule):
            self.menu_modules_add.Enable(False)
        else:
            self.menu_modules_delete.Enable(False)
            self.menu_modules_edit.Enable(False)


    def onEditModuleApply( self, event ):
        module = event.data
        module_name = event.module_name
                
        if self.edit_state=='add':
            # get library path
            library_path = ''
            module_path = os.path.join(module.source_path, module_name)
            try:
                self.manager_module.CreateFile(module_path, module.content)
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), 'Error creating module', wx.OK | wx.ICON_ERROR)                                    
                return
            
        elif self.edit_state=='edit':
            # change library name if changed on disk
            library_path = os.path.dirname(module.source_path)
            module_path = os.path.normpath(os.path.join(library_path, module_name))
            
            if os.path.normpath(module.source_path)!=module_path:
                # file was renamed
                if self.tree_modules.GetSelection().IsOk():
                    moduleobj = self.tree_modules_manager.ItemToObject(self.tree_modules.GetSelection())
                    try:
                        moduleobj.module = self.manager_module.MoveFile(module.source_path, os.path.join(library_path, module_name))
                    except Exception as e:
                        print_stack()
                        wx.MessageBox(format(e), 'Error renaming module', wx.OK | wx.ICON_ERROR)                                    
                        return
            try:
                if module.content:
                    self.manager_module.EditFile(module_path, module.content, create=True)
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), 'Error editing module', wx.OK | wx.ICON_ERROR)                                    
                return
            
        else:
            return
        
        self.manager_module.EditMetadata(module_path, module.metadata)
        
        self.edit_state = None
        self.show_module(module)

        self.load()

    def onEditModuleCancel( self, event ):
        module = None
        item = self.tree_modules.GetSelection()
        if item.IsOk():
            obj = self.tree_modules_manager.ItemToObject(item)
            if isinstance(obj, DataModelModule):
                module = obj.module                
        self.edit_state = None
        self.show_module(module)
    
    def onToggleModulePathClicked( self, event ):
        self.show_module_path = self.toolbar_module.GetToolState(self.toggle_module_path.GetId())
        self.load()
        
    def onToggleShowBothChangesClicked( self, event ):
        self.show_both_changes = self.toolbar_module.GetToolState(self.toggle_show_both_changes.GetId())
        self.load()
    
    def onToggleShowConflictChangesClicked( self, event ):
        self.show_conflict_changes = self.toolbar_module.GetToolState(self.toggle_show_conflict_changes.GetId())
        self.load()
    
    def onToggleShowIncomingChangesClicked( self, event ):
        self.show_incoming_changes = self.toolbar_module.GetToolState(self.toggle_show_incoming_changes.GetId())
        self.load()
    
    def onToggleShowOutgoingChangesClicked( self, event ):
        self.show_outgoing_changes = self.toolbar_module.GetToolState(self.toggle_show_outgoing_changes.GetId())
        self.load()

    def onButtonRefreshModulesClick( self, event ):
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
                self.manager_module.CreateFolder(os.path.join(path, name))
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
                self.manager_module.CreateFolder(os.path.join(path, name+".module"))
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
                    self.manager_module.MoveFolder(path, newpath)
                except Exception as e:
                    print_stack()
                    wx.MessageBox(format(e), 'Error renaming folder', wx.OK | wx.ICON_ERROR)
            dlg.Destroy()
        elif isinstance(obj, DataModelLibrary):
            dlg = wx.TextEntryDialog(self, 'Enter new library name', 'Rename library')
            if dlg.ShowModal() == wx.ID_OK:
                name = dlg.GetValue()
                try:
                    newpath = os.path.join(os.path.dirname(path), name+".module")
                    self.manager_module.MoveFolder(path, newpath)
                except Exception as e:
                    print_stack()
                    wx.MessageBox(format(e), 'Error renaming library', wx.OK | wx.ICON_ERROR)
            dlg.Destroy()
        
        self.load()

    def onMenuLibrariesRemove( self, event ):
        item = self.tree_libraries.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_libraries_manager.ItemToObject(item)
        path = obj.path
        try:
            self.manager_module.DeleteFolder(path)
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Error removing %s:'%path, wx.OK | wx.ICON_ERROR)
        self.load()
        

    def onMenuLibrariesAddModule( self, event ):
        item = self.tree_libraries.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_libraries_manager.ItemToObject(item)
        if isinstance(obj, DataModelLibrary)==False:
            return

        self.edit_state = 'add'
        self.new_module(obj.path)


    def onMenuModulesUpdate( self, event ):
        files = []
        for item in self.tree_modules.GetSelections():
            obj = self.tree_modules_manager.ItemToObject(item)
            if isinstance(obj, DataModelModule):
                files.append(obj.module)
            elif isinstance(obj, DataModelModulePath):
                for child in obj.childs:
                    if isinstance(child, DataModelModule):
                        files.append(child.module)
        
        try:
            self.manager_module.Update(files) 
            self.load()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Upload failed', wx.OK | wx.ICON_ERROR)
    
    def onMenuModulesForceUpdate( self, event ):
        files = []
        for item in self.tree_modules.GetSelections():
            obj = self.tree_modules_manager.ItemToObject(item)
            if isinstance(obj, DataModelModule):
                files.append(obj.module)
            elif isinstance(obj, DataModelModulePath):
                if obj.childs:
                    for child in obj.childs:
                        if isinstance(child, DataModelModule):
                            files.append(child.module)
        
        try:
            if len(files)>0:
                self.manager_module.Update(files, force=True) 
            self.load()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Upload failed', wx.OK | wx.ICON_ERROR)
    
    def onMenuModulesCommit( self, event ):
        files = []
        for item in self.tree_modules.GetSelections():
            obj = self.tree_modules_manager.ItemToObject(item)
            if isinstance(obj, DataModelModule):
                files.append(obj.module)
            elif isinstance(obj, DataModelModulePath):
                for child in obj.childs:
                    if isinstance(child, DataModelModule):
                        files.append(child.module)
        
        try:
            self.manager_module.Commit(files) 
            self.load()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Commit failed', wx.OK | wx.ICON_ERROR)
            
    
    def onMenuModulesForceCommit( self, event ):
        files = []
        for item in self.tree_modules.GetSelections():
            obj = self.tree_modules_manager.ItemToObject(item)
            if isinstance(obj, DataModelModule):
                files.append(obj.module)
            elif isinstance(obj, DataModelModulePath):
                for child in obj.childs:
                    if isinstance(child, DataModelModule):
                        files.append(child.module)
        
        try:
            self.manager_module.Commit(files, force=True) 
            self.load()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Commit failed', wx.OK | wx.ICON_ERROR)

    def onMenuModulesAdd( self, event ):
        item = self.tree_modules.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_modules_manager.ItemToObject(item)
        if isinstance(obj, DataModelModulePath)==False:
            return

        self.edit_state = 'add'
        self.new_module(obj.path)
    
    def onMenuModulesEdit( self, event ):
        item = self.tree_modules.GetSelection()
        if item.IsOk()==False:
            return
        moduleobj = self.tree_modules_manager.ItemToObject(item)
        if isinstance(moduleobj, DataModelModule)==False:
            return
        state = moduleobj.module.state
        if state.rfind('income')!=-1 or state.rfind('conflict')!=-1:
            wx.MessageBox("Item should be updated prior to beeing edited", 'Can not edit', wx.OK | wx.ICON_ERROR)
            return
        
        self.edit_state = 'edit'
    
        self.edit_module(moduleobj.module)
    
    def onMenuModulesDelete( self, event ):
        files = []
        for item in self.tree_modules.GetSelections():
            obj = self.tree_modules_manager.ItemToObject(item)
            if isinstance(obj, DataModelModule):
                files.append(obj.module)
            elif isinstance(obj, DataModelModulePath):
                pass
        
        try:
            for file in files:
                self.manager_module.DeleteFile(file) 
            self.load()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Delete failed', wx.OK | wx.ICON_ERROR)

    def onSearchModulesButton( self, event ):
        return self.onSearchModulesTextEnter(event)
    
    def onSearchModulesTextEnter( self, event ):
        # set search filter
        self.modules_filter.remove('search')
        if self.search_modules.Value!='':
            self.modules_filter.add('search', self.search_modules.Value)
        # apply new filter and reload
        self.loadModules()
