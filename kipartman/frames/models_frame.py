from dialogs.panel_models import PanelModels
from frames.edit_model_frame import EditModelFrame, EVT_EDIT_FOOTPRINT_APPLY_EVENT, EVT_EDIT_FOOTPRINT_CANCEL_EVENT
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


class DataModelModelPath(helper.tree.TreeContainerItem):
    _type_ = 3
    image_none = None
    
    def __init__(self, path):
        super(DataModelModelPath, self).__init__()
        self.path = path
        
        if not DataModelModelPath.image_none:
            DataModelModelPath.image_none = wx.Bitmap()
            DataModelModelPath.image_none.FromRGBA(11, 10, red=0, green=0, blue=0, alpha=0)
        
    def GetValue(self, col):
        if col==0:
            return DataModelModelPath.image_none
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

class DataModelModel(helper.tree.TreeItem):
    _type_ = 4
    def __init__(self, imagelist, path, model):
        super(DataModelModel, self).__init__()
        self.imagelist = imagelist
        self.path = path
        self.model = model

    def GetValue(self, col):
        if col==0:
            return self.imagelist.GetBitmap(self.model.state)
        elif col==1:
            version = ''
            if self.model.version:
                version = str(self.model.version)
            return version
        elif col==2:
            if self.parent:
                name = os.path.basename(self.model.source_path).replace(".mod", "")
            else:
                name = os.path.join(self.path, os.path.basename(self.model.source_path).replace(".mod", ""))
            return name

        return None

#    def GetDragData(self):
#        if isinstance(self.parent, DataModelCategoryPath):
#            return {'id': self.model.id}
#        return None

class TreeManagerModels(helper.tree.TreeManager):
    def __init__(self, tree_view, *args, **kwargs):
        super(TreeManagerModels, self).__init__(tree_view, *args, **kwargs)
        self.imagelist = TreeImageList(11, 10)
                
    def FindPath(self, path):
        path = os.path.normpath(path)
        for data in self.data:
#            if isinstance(data, DataModelModelPath) and data.path==os.path.normpath(path):
            if isinstance(data, DataModelModelPath) and data.path==path:
                return data
        return None

    def FindModel(self, path, model):
        path = os.path.normpath(path)
        for data in self.data:
#            if data._type_==DataModelModel._type_ and data.path==path and data.model==model:
            if isinstance(data, DataModelModel) and data.path==os.path.normpath(path) and data.model==model:
                return data
        return None

    def AppendPath(self, path):
        pathobj = self.FindPath(path)
        if pathobj:
            return pathobj
        pathobj = DataModelModelPath(path)
        parentpath = self.FindPath(os.path.dirname(path))
        self.AppendItem(parentpath, pathobj)
        return pathobj

    def AppendModel(self, path, model, flat=False):
        pathobj = None
        if flat==False:
            pathobj = self.FindPath(path)
        modelobj = DataModelModel(self.imagelist, path, model)
        self.AppendItem(pathobj, modelobj)
        return modelobj

    def UpdateModel(self, path, model):
        modelobj = self.FindModel(path, model)
        if modelobj:
            self.UpdateItem(modelobj)
        return modelobj

    def DeleteModel(self, path, model):
        pathobj = self.FindPath(path)
        modelobj = DataModelModel(self.imagelist, path, model)
        self.DeleteItem(pathobj, modelobj)

class ModelsFrameFilter(Filter):
    def __init__(self, filters_panel, onRemove):
        super(ModelsFrameFilter, self).__init__(filters_panel, onRemove)

    def model_search(self, model, value):
        if model.source_path.rfind(value)>-1:
            return True
        if model.metadata and model.metadata.rfind(value)>-1:
            metadata = json.loads(model.metadata)
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

    def FilterModel(self, model):
        if len(self.filters)==0:
            return False

        for filter_name in self.filters:
            filter = self.filters[filter_name]
            
            if filter['name']=='path' and model.source_path.startswith(filter['value']+os.path.sep):
                return False

            if filter['name']=='search' and self.model_search(model, filter['value']):
                return False

        return True

class ModelsFrame(PanelModels): 
    def __init__(self, parent):
        super(ModelsFrame, self).__init__(parent)
        
        self.file_manager_lib = KicadFileManagerLib()
        self.manager_lib = sync.version_manager.VersionManager(self.file_manager_lib)
        self.file_manager_lib.AddChangeHook(self.onFileLibChanged)
        
        # create libraries data
        self.tree_libraries_manager = TreeManagerLibraries(self.tree_libraries, context_menu=self.menu_libraries)
        self.tree_libraries_manager.AddTextColumn("name")
        self.tree_libraries_manager.OnSelectionChanged = self.onTreeLibrariesSelChanged
        self.tree_libraries_manager.OnItemBeforeContextMenu = self.onTreeLibrariesBeforeContextMenu

        # models filters
        self.models_filter = ModelsFrameFilter(self.filters_panel, self.onButtonRemoveFilterClick)

        # create model list
        self.tree_models_manager = TreeManagerModels(self.tree_models, context_menu=self.menu_models)
        self.tree_models_manager.AddBitmapColumn("s")
        self.tree_models_manager.AddIntegerColumn("v")
        self.tree_models_manager.AddTextColumn("name")
        self.tree_models_manager.OnSelectionChanged = self.onTreeModelsSelChanged
        self.tree_models_manager.OnItemBeforeContextMenu = self.onTreeModelsBeforeContextMenu

        self.tree_models_manager.imagelist.AddFile('', 'resources/none.png')
        self.tree_models_manager.imagelist.AddFile(None, 'resources/none.png')
        self.tree_models_manager.imagelist.AddFile('conflict_add', 'resources/conflict_add.png')
        self.tree_models_manager.imagelist.AddFile('conflict_change', 'resources/conflict_change.png')
        self.tree_models_manager.imagelist.AddFile('conflict_del', 'resources/conflict_del.png')
        self.tree_models_manager.imagelist.AddFile('income_add', 'resources/income_add.png')
        self.tree_models_manager.imagelist.AddFile('income_change', 'resources/income_change.png')
        self.tree_models_manager.imagelist.AddFile('income_del', 'resources/income_del.png')
        self.tree_models_manager.imagelist.AddFile('outgo_add', 'resources/outgo_add.png')
        self.tree_models_manager.imagelist.AddFile('outgo_change', 'resources/outgo_change.png')
        self.tree_models_manager.imagelist.AddFile('outgo_del', 'resources/outgo_del.png')
        #self.tree_models_manager.imagelist.AddFile('prop_changed', 'resources/prop_changed.png')

        # create edit model panel
        self.panel_edit_model = EditModelFrame(self.model_splitter)
        self.model_splitter.SplitHorizontally(self.model_splitter.Window1, self.panel_edit_model, 400)
        self.panel_edit_model.Bind( EVT_EDIT_FOOTPRINT_APPLY_EVENT, self.onEditModelApply )
        self.panel_edit_model.Bind( EVT_EDIT_FOOTPRINT_CANCEL_EVENT, self.onEditModelCancel )

        self.toolbar_model.ToggleTool(self.toggle_model_path.GetId(), True)
        
        self.show_model_path = self.toolbar_model.GetToolState(self.toggle_model_path.GetId())
        self.previous_show_model_path = self. show_model_path
        
        self.show_both_changes = self.toolbar_model.GetToolState(self.toggle_show_both_changes.GetId())
        self.show_conflict_changes = self.toolbar_model.GetToolState(self.toggle_show_conflict_changes.GetId())
        self.show_incoming_changes = self.toolbar_model.GetToolState(self.toggle_show_incoming_changes.GetId())
        self.show_outgoing_changes = self.toolbar_model.GetToolState(self.toggle_show_outgoing_changes.GetId())
    
        # initial edit state
        self.show_model(None)
        self.edit_state = None

        self.load() 
        
    def load(self):
        try:
            self.models = self.manager_lib.Synchronize()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Synchronization with kipartbase failed, check your connection and try again', wx.OK | wx.ICON_ERROR)                                    
        
        self.loadLibraries()
        self.loadModels()
    
    def loadLibraries(self):
        
        self.tree_libraries_manager.SaveState()
        
        # load libraries tree
        for model_path in self.models:
            # decompose path
            folders = []
            library_path = os.path.dirname(model_path)
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

    def loadModels(self):
            
        if self.previous_show_model_path!=self.show_model_path:
            # in case switch from tree to flat view 
            self.tree_models_manager.ClearItems()
            self.previous_show_model_path = self.show_model_path
            
        self.tree_models_manager.SaveState()
        
        # load models from local folder
        for model_path in self.models:
            library_path = os.path.dirname(model_path)
            if self.show_model_path==True:
                pathobj = self.tree_models_manager.FindPath(library_path)
                if self.models_filter.FilterPath(library_path)==False:
                    if self.tree_models_manager.DropStateObject(pathobj)==False:
                        self.tree_models_manager.AppendPath(library_path)

            model = self.models[model_path]
            parent = library_path

            if self.show_both_changes==False and self.show_conflict_changes==False and self.show_incoming_changes==False and self.show_outgoing_changes==False:
                show = True
            else:
                show = False
            if self.show_both_changes==True and model.state.rfind('outgo_')!=-1:
                show = True
            if self.show_both_changes==True and model.state.rfind('income_')!=-1:
                show = True
            if self.show_conflict_changes==True and model.state.rfind('conflict_')!=-1:
                show = True
            if self.show_incoming_changes==True and model.state.rfind('income_')!=-1:
                show = True
            if self.show_outgoing_changes==True and model.state.rfind('outgo_')!=-1:
                show = True

            libraryobj = self.tree_models_manager.FindModel(parent, model)
            if show==True:
                if self.models_filter.FilterModel(model)==False:
                    if self.tree_models_manager.DropStateObject(libraryobj)==False:
                        if self.show_model_path==True:
                            self.tree_models_manager.AppendModel(parent, model, flat=False)
                        else:
                            self.tree_models_manager.AppendModel(parent, model, flat=True)
                
        self.tree_models_manager.PurgeState()

    def show_model(self, model):
        # disable editing
        self.panel_edit_model.enable(False)
        # enable evrything else
        self.panel_path.Enabled = True
        self.panel_models.Enabled = True
        # set part
        self.panel_edit_model.SetModel(model)

    def edit_model(self, model):
        self.show_model(model)
        # enable editing
        self.panel_edit_model.enable(True)
        # disable evrything else
        self.panel_path.Enabled = False
        self.panel_models.Enabled = False
        
    def new_model(self, path):
        model = rest.model.VersionedFile()
        model.source_path = path         
        self.edit_model(model)

    def onFileLibChanged(self, event):
        # do a synchronize when a file change on disk
        print "-------------------------------------------------------------------------------------"
        self.load()
       
    def onTreeLibrariesSelChanged( self, event ):
        item = self.tree_libraries.GetSelection()
        if item.IsOk()==False:
            return    
        pathobj = self.tree_libraries_manager.ItemToObject(item)
        # set category filter
        self.models_filter.remove('path')
        if pathobj:
            self.models_filter.add('path', pathobj.path, pathobj.path)
        # apply new filter and reload
        self.loadModels()

    def onTreeLibrariesBeforeContextMenu( self, event ):
        item = self.tree_libraries.GetSelection()
        if item.IsOk()==False:
            return    
        obj = self.tree_libraries_manager.ItemToObject(item)

        self.menu_libraries_add_folder.Enable(True)
        self.menu_libraries_add_library.Enable(True)
        self.menu_libraries_add_model.Enable(True)
        if isinstance(obj, DataModelLibrary):
            self.menu_libraries_add_folder.Enable(False)
            self.menu_libraries_add_library.Enable(False)
        else:
            self.menu_libraries_add_model.Enable(False)


    def onButtonRemoveFilterClick( self, event ):
        button = event.GetEventObject()
        self.models_filter.remove(button.GetName())
        self.tree_libraries.UnselectAll()
        self.loadModels()

    def onTreeModelsSelChanged( self, event ):
        if self.edit_state:
            return
        item = self.tree_models.GetSelection()
        if item.IsOk()==False:
            return
        modelobj = self.tree_models_manager.ItemToObject(item)
        if isinstance(modelobj, DataModelModel)==False:
            self.show_model(None)
            return
        self.panel_edit_model.SetModel(modelobj.model)

        self.show_model(modelobj.model)

    def onTreeModelsBeforeContextMenu( self, event ):
        item = self.tree_models.GetSelection()
        if item.IsOk()==False:
            return    
        obj = self.tree_models_manager.ItemToObject(item)

        self.menu_models_add.Enable(True)
        self.menu_models_delete.Enable(True)
        self.menu_models_edit.Enable(True)
        if isinstance(obj, DataModelModel):
            self.menu_models_add.Enable(False)
        else:
            self.menu_models_delete.Enable(False)
            self.menu_models_edit.Enable(False)


    def onEditModelApply( self, event ):
        model = event.data
        model_name = event.model_name
                
        if self.edit_state=='add':
            # get library path
            library_path = ''
            model_path = os.path.join(model.source_path, model_name)
            try:
                self.manager_lib.CreateFile(model_path, model.content)
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), 'Error creating model', wx.OK | wx.ICON_ERROR)                                    
                return
            
        elif self.edit_state=='edit':
            # change library name if changed on disk
            library_path = os.path.dirname(model.source_path)
            model_path = os.path.normpath(os.path.join(library_path, model_name))
            
            if os.path.normpath(model.source_path)!=model_path:
                # file was renamed
                if self.tree_models.GetSelection().IsOk():
                    modelobj = self.tree_models_manager.ItemToObject(self.tree_models.GetSelection())
                    try:
                        modelobj.model = self.manager_lib.MoveFile(model.source_path, os.path.join(library_path, model_name))
                    except Exception as e:
                        print_stack()
                        wx.MessageBox(format(e), 'Error renaming model', wx.OK | wx.ICON_ERROR)                                    
                        return
            try:
                if model.content:
                    self.manager_lib.EditFile(model_path, model.content, create=True)
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), 'Error editing model', wx.OK | wx.ICON_ERROR)                                    
                return
            
        else:
            return
        
        self.manager_lib.EditMetadata(model_path, model.metadata)
        
        self.edit_state = None
        self.show_model(model)

        self.load()

    def onEditModelCancel( self, event ):
        model = None
        item = self.tree_models.GetSelection()
        if item.IsOk():
            obj = self.tree_models_manager.ItemToObject(item)
            if isinstance(obj, DataModelModel):
                model = obj.model                
        self.edit_state = None
        self.show_model(model)
    
    def onToggleModelPathClicked( self, event ):
        self.show_model_path = self.toolbar_model.GetToolState(self.toggle_model_path.GetId())
        self.load()
        
    def onToggleShowBothChangesClicked( self, event ):
        self.show_both_changes = self.toolbar_model.GetToolState(self.toggle_show_both_changes.GetId())
        self.load()
    
    def onToggleShowConflictChangesClicked( self, event ):
        self.show_conflict_changes = self.toolbar_model.GetToolState(self.toggle_show_conflict_changes.GetId())
        self.load()
    
    def onToggleShowIncomingChangesClicked( self, event ):
        self.show_incoming_changes = self.toolbar_model.GetToolState(self.toggle_show_incoming_changes.GetId())
        self.load()
    
    def onToggleShowOutgoingChangesClicked( self, event ):
        self.show_outgoing_changes = self.toolbar_model.GetToolState(self.toggle_show_outgoing_changes.GetId())
        self.load()

    def onButtonRefreshModelsClick( self, event ):
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
        

    def onMenuLibrariesAddModel( self, event ):
        item = self.tree_libraries.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_libraries_manager.ItemToObject(item)
        if isinstance(obj, DataModelLibrary)==False:
            return

        self.edit_state = 'add'
        self.new_model(obj.path)


    def onMenuModelsUpdate( self, event ):
        files = []
        for item in self.tree_models.GetSelections():
            obj = self.tree_models_manager.ItemToObject(item)
            if isinstance(obj, DataModelModel):
                files.append(obj.model)
            elif isinstance(obj, DataModelModelPath):
                for child in obj.childs:
                    if isinstance(child, DataModelModel):
                        files.append(child.model)
        
        try:
            self.manager_lib.Update(files) 
            self.load()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Upload failed', wx.OK | wx.ICON_ERROR)
    
    def onMenuModelsForceUpdate( self, event ):
        files = []
        for item in self.tree_models.GetSelections():
            obj = self.tree_models_manager.ItemToObject(item)
            if isinstance(obj, DataModelModel):
                files.append(obj.model)
            elif isinstance(obj, DataModelModelPath):
                if obj.childs:
                    for child in obj.childs:
                        if isinstance(child, DataModelModel):
                            files.append(child.model)
        
        try:
            if len(files)>0:
                self.manager_lib.Update(files, force=True) 
            self.load()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Upload failed', wx.OK | wx.ICON_ERROR)
    
    def onMenuModelsCommit( self, event ):
        files = []
        for item in self.tree_models.GetSelections():
            obj = self.tree_models_manager.ItemToObject(item)
            if isinstance(obj, DataModelModel):
                files.append(obj.model)
            elif isinstance(obj, DataModelModelPath):
                for child in obj.childs:
                    if isinstance(child, DataModelModel):
                        files.append(child.model)
        
        try:
            print "*****", files
            self.manager_lib.Commit(files) 
            self.load()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Commit failed', wx.OK | wx.ICON_ERROR)
            
    
    def onMenuModelsForceCommit( self, event ):
        files = []
        for item in self.tree_models.GetSelections():
            obj = self.tree_models_manager.ItemToObject(item)
            if isinstance(obj, DataModelModel):
                files.append(obj.model)
            elif isinstance(obj, DataModelModelPath):
                for child in obj.childs:
                    if isinstance(child, DataModelModel):
                        files.append(child.model)
        
        try:
            self.manager_lib.Commit(files, force=True) 
            self.load()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Commit failed', wx.OK | wx.ICON_ERROR)

    def onMenuModelsAdd( self, event ):
        item = self.tree_models.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_models_manager.ItemToObject(item)
        if isinstance(obj, DataModelModelPath)==False:
            return

        self.edit_state = 'add'
        self.new_model(obj.path)
    
    def onMenuModelsEdit( self, event ):
        item = self.tree_models.GetSelection()
        if item.IsOk()==False:
            return
        modelobj = self.tree_models_manager.ItemToObject(item)
        if isinstance(modelobj, DataModelModel)==False:
            return
        state = modelobj.model.state
        if state.rfind('income')!=-1 or state.rfind('conflict')!=-1:
            wx.MessageBox("Item should be updated prior to beeing edited", 'Can not edit', wx.OK | wx.ICON_ERROR)
            return
        
        self.edit_state = 'edit'
    
        self.edit_model(modelobj.model)
    
    def onMenuModelsDelete( self, event ):
        files = []
        for item in self.tree_models.GetSelections():
            obj = self.tree_models_manager.ItemToObject(item)
            if isinstance(obj, DataModelModel):
                files.append(obj.model)
            elif isinstance(obj, DataModelModelPath):
                pass
        
        try:
            for file in files:
                self.manager_lib.DeleteFile(file) 
            self.load()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Delete failed', wx.OK | wx.ICON_ERROR)

    def onSearchModelsButton( self, event ):
        print "####"
        return self.onSearchModelsTextEnter(event)
    
    def onSearchModelsTextEnter( self, event ):
        # set search filter
        self.models_filter.remove('search')
        if self.search_models.Value!='':
            self.models_filter.add('search', self.search_models.Value)
        # apply new filter and reload
        self.loadModels()
