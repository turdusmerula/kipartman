from dialogs.panel_footprints import PanelFootprints
from frames.edit_footprint_frame import EditFootprintFrame, EVT_EDIT_FOOTPRINT_APPLY_EVENT, EVT_EDIT_FOOTPRINT_CANCEL_EVENT
from kicad.kicad_file_manager import KicadFileManagerPretty
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


class DataModelFootprintPath(helper.tree.TreeContainerItem):
    image_none = None
    
    def __init__(self, path):
        super(DataModelFootprintPath, self).__init__()
        self.path = path
        
        if not DataModelFootprintPath.image_none:
            DataModelFootprintPath.image_none = wx.Bitmap()
            DataModelFootprintPath.image_none.FromRGBA(11, 10, red=0, green=0, blue=0, alpha=0)
        
    def GetValue(self, col):
        if col==0:
            return DataModelFootprintPath.image_none
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

class DataModelFootprint(helper.tree.TreeItem):
    def __init__(self, imagelist, path, footprint):
        super(DataModelFootprint, self).__init__()
        self.imagelist = imagelist
        self.path = path
        self.footprint = footprint

    def GetValue(self, col):
        version = ''
        if self.footprint.version:
            version = str(self.footprint.version)
        if self.parent:
            name = os.path.basename(self.footprint.source_path).replace(".kicad_mod", "")
        else:
            name = os.path.join(self.path, os.path.basename(self.footprint.source_path).replace(".kicad_mod", ""))
        vMap = {
            0 : self.imagelist.GetBitmap(self.footprint.state), 
            1 : str(version),
            2 : name,
        }
#        return wx.dataview.DataViewIconText(vMap[col], None)
        return vMap[col]

#    def GetDragData(self):
#        if isinstance(self.parent, DataModelCategoryPath):
#            return {'id': self.footprint.id}
#        return None

class TreeManagerFootprints(helper.tree.TreeManager):
    def __init__(self, tree_view, *args, **kwargs):
        super(TreeManagerFootprints, self).__init__(tree_view, *args, **kwargs)
        self.imagelist = TreeImageList(11, 10)
                
    def FindPath(self, path):
        for data in self.data:
            if isinstance(data, DataModelFootprintPath) and data.path==os.path.normpath(path):
                return data
        return None

    def FindFootprint(self, path, footprint):
        for data in self.data:
            if isinstance(data, DataModelFootprint) and data.path==os.path.normpath(path) and data.footprint==footprint:
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

    def AppendFootprint(self, path, footprint, flat=False):
        pathobj = None
        if flat==False:
            pathobj = self.FindPath(path)
        footprintobj = DataModelFootprint(self.imagelist, path, footprint)
        self.AppendItem(pathobj, footprintobj)
        return footprintobj

    def UpdateFootprint(self, path, footprint):
        footprintobj = self.FindFootprint(path, footprint)
        if footprintobj:
            self.UpdateItem(footprintobj)
        return footprintobj

    def DeleteFootprint(self, path, footprint):
        pathobj = self.FindPath(path)
        footprintobj = DataModelFootprint(self.imagelist, path, footprint)
        self.DeleteItem(pathobj, footprintobj)

class FootprintsFrameFilter(Filter):
    def __init__(self, filters_panel, onRemove):
        super(FootprintsFrameFilter, self).__init__(filters_panel, onRemove)

    def footprint_search(self, footprint, value):
        if footprint.source_path.rfind(value)>-1:
            return True
        if footprint.metadata and footprint.metadata.rfind(value)>-1:
            metadata = json.loads(footprint.metadata)
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

    def FilterFootprint(self, footprint):
        if len(self.filters)==0:
            return False

        for filter_name in self.filters:
            filter = self.filters[filter_name]
            
            if filter['name']=='path' and footprint.source_path.startswith(filter['value']+os.path.sep):
                return False

            if filter['name']=='search' and self.footprint_search(footprint, filter['value']):
                return False

        return True

class FootprintsFrame(PanelFootprints): 
    def __init__(self, parent):
        super(FootprintsFrame, self).__init__(parent)
        
        self.file_manager_pretty = KicadFileManagerPretty()
        self.manager_pretty = sync.version_manager.VersionManager(self.file_manager_pretty)
        self.manager_pretty.on_change_hook = self.onFilePrettyChanged
        
        # create libraries data
        self.tree_libraries_manager = TreeManagerLibraries(self.tree_libraries, context_menu=self.menu_libraries)
        self.tree_libraries_manager.AddTextColumn("name")
        self.tree_libraries_manager.OnSelectionChanged = self.onTreeLibrariesSelChanged
        self.tree_libraries_manager.OnItemBeforeContextMenu = self.onTreeLibrariesBeforeContextMenu

        # footprints filters
        self.footprints_filter = FootprintsFrameFilter(self.filters_panel, self.onButtonRemoveFilterClick)

        # create footprint list
        self.tree_footprints_manager = TreeManagerFootprints(self.tree_footprints, context_menu=self.menu_footprints)
        self.tree_footprints_manager.AddBitmapColumn("s")
        self.tree_footprints_manager.AddIntegerColumn("v")
        self.tree_footprints_manager.AddTextColumn("name")
        self.tree_footprints_manager.OnSelectionChanged = self.onTreeFootprintsSelChanged
        self.tree_footprints_manager.OnItemBeforeContextMenu = self.onTreeFootprintsBeforeContextMenu

        self.tree_footprints_manager.imagelist.AddFile('', 'resources/none.png')
        self.tree_footprints_manager.imagelist.AddFile(None, 'resources/none.png')
        self.tree_footprints_manager.imagelist.AddFile('conflict_add', 'resources/conflict_add.png')
        self.tree_footprints_manager.imagelist.AddFile('conflict_change', 'resources/conflict_change.png')
        self.tree_footprints_manager.imagelist.AddFile('conflict_del', 'resources/conflict_del.png')
        self.tree_footprints_manager.imagelist.AddFile('income_add', 'resources/income_add.png')
        self.tree_footprints_manager.imagelist.AddFile('income_change', 'resources/income_change.png')
        self.tree_footprints_manager.imagelist.AddFile('income_del', 'resources/income_del.png')
        self.tree_footprints_manager.imagelist.AddFile('outgo_add', 'resources/outgo_add.png')
        self.tree_footprints_manager.imagelist.AddFile('outgo_change', 'resources/outgo_change.png')
        self.tree_footprints_manager.imagelist.AddFile('outgo_del', 'resources/outgo_del.png')
        #self.tree_footprints_manager.imagelist.AddFile('prop_changed', 'resources/prop_changed.png')

        # create edit footprint panel
        self.panel_edit_footprint = EditFootprintFrame(self.footprint_splitter)
        self.footprint_splitter.SplitHorizontally(self.footprint_splitter.Window1, self.panel_edit_footprint, 400)
        self.panel_edit_footprint.Bind( EVT_EDIT_FOOTPRINT_APPLY_EVENT, self.onEditFootprintApply )
        self.panel_edit_footprint.Bind( EVT_EDIT_FOOTPRINT_CANCEL_EVENT, self.onEditFootprintCancel )

        self.toolbar_footprint.ToggleTool(self.toggle_footprint_path.GetId(), True)
        
        self.show_footprint_path = self.toolbar_footprint.GetToolState(self.toggle_footprint_path.GetId())
        self.previous_show_footprint_path = self. show_footprint_path
        
        self.show_both_changes = self.toolbar_footprint.GetToolState(self.toggle_show_both_changes.GetId())
        self.show_conflict_changes = self.toolbar_footprint.GetToolState(self.toggle_show_conflict_changes.GetId())
        self.show_incoming_changes = self.toolbar_footprint.GetToolState(self.toggle_show_incoming_changes.GetId())
        self.show_outgoing_changes = self.toolbar_footprint.GetToolState(self.toggle_show_outgoing_changes.GetId())
    
        # initial edit state
        self.show_footprint(None)
        self.edit_state = None

        self.load() 
        
    def load(self):
        try:
            self.footprints = self.manager_pretty.Synchronize()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Synchronization with kipartbase failed, check your connection and try again', wx.OK | wx.ICON_ERROR)                                    
            
        #self.footprints = self.manager_pretty.
        #self.footprints =  self.resource_pretty.Synchronize()
        
        self.loadLibraries()
        self.loadFootprints()
    
    def loadLibraries(self):
        
        self.tree_libraries_manager.SaveState()
        
        # load libraries tree
        for footprint_path in self.footprints:
            # decompose path
            folders = []
            library_path = os.path.dirname(footprint_path)
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
        for folder in self.file_manager_pretty.folders:
            if re.compile("^.*\.pretty$").match(os.path.normpath(os.path.abspath(folder))):
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

    def loadFootprints(self):
            
        if self.previous_show_footprint_path!=self.show_footprint_path:
            # in case switch from tree to flat view 
            self.tree_footprints_manager.ClearItems()
            self.previous_show_footprint_path = self.show_footprint_path
            
        self.tree_footprints_manager.SaveState()
        
        # load footprints from local folder
        for footprint_path in self.footprints:
            library_path = os.path.dirname(footprint_path)
            if self.show_footprint_path==True:
                pathobj = self.tree_footprints_manager.FindPath(library_path)
                if self.footprints_filter.FilterPath(library_path)==False:
                    if self.tree_footprints_manager.DropStateObject(pathobj)==False:
                        self.tree_footprints_manager.AppendPath(library_path)

            footprint = self.footprints[footprint_path]
            parent = library_path

            if self.show_both_changes==False and self.show_conflict_changes==False and self.show_incoming_changes==False and self.show_outgoing_changes==False:
                show = True
            else:
                show = False
            if self.show_both_changes==True and footprint.state.rfind('outgo_')!=-1:
                show = True
            if self.show_both_changes==True and footprint.state.rfind('income_')!=-1:
                show = True
            if self.show_conflict_changes==True and footprint.state.rfind('conflict_')!=-1:
                show = True
            if self.show_incoming_changes==True and footprint.state.rfind('income_')!=-1:
                show = True
            if self.show_outgoing_changes==True and footprint.state.rfind('outgo_')!=-1:
                show = True

            libraryobj = self.tree_footprints_manager.FindFootprint(parent, footprint)
            if show==True:
                if self.footprints_filter.FilterFootprint(footprint)==False:
                    if self.tree_footprints_manager.DropStateObject(libraryobj)==False:
                        if self.show_footprint_path==True:
                            self.tree_footprints_manager.AppendFootprint(parent, footprint, flat=False)
                        else:
                            self.tree_footprints_manager.AppendFootprint(parent, footprint, flat=True)
                
        self.tree_footprints_manager.PurgeState()

    def show_footprint(self, footprint):
        # disable editing
        self.panel_edit_footprint.enable(False)
        # enable evrything else
        self.panel_path.Enabled = True
        self.panel_footprints.Enabled = True
        # set part
        self.panel_edit_footprint.SetFootprint(footprint)

    def edit_footprint(self, footprint):
        self.show_footprint(footprint)
        # enable editing
        self.panel_edit_footprint.enable(True)
        # disable evrything else
        self.panel_path.Enabled = False
        self.panel_footprints.Enabled = False
        
    def new_footprint(self, path):
        footprint = rest.model.VersionedFile()
        footprint.source_path = path         
        self.edit_footprint(footprint)

    def onFilePrettyChanged(self, event):
        # do a synchronize when a file change on disk
        self.load()
       
    def onTreeLibrariesSelChanged( self, event ):
        item = self.tree_libraries.GetSelection()
        if item.IsOk()==False:
            return    
        pathobj = self.tree_libraries_manager.ItemToObject(item)
        # set category filter
        self.footprints_filter.remove('path')
        if pathobj:
            self.footprints_filter.add('path', pathobj.path, pathobj.path)
        # apply new filter and reload
        self.loadFootprints()

    def onTreeLibrariesBeforeContextMenu( self, event ):
        item = self.tree_libraries.GetSelection()
        if item.IsOk()==False:
            return    
        obj = self.tree_libraries_manager.ItemToObject(item)

        self.menu_libraries_add_folder.Enable(True)
        self.menu_libraries_add_library.Enable(True)
        self.menu_libraries_add_footprint.Enable(True)
        if isinstance(obj, DataModelLibrary):
            self.menu_libraries_add_folder.Enable(False)
            self.menu_libraries_add_library.Enable(False)
        else:
            self.menu_libraries_add_footprint.Enable(False)


    def onButtonRemoveFilterClick( self, event ):
        button = event.GetEventObject()
        self.footprints_filter.remove(button.GetName())
        self.tree_libraries.UnselectAll()
        self.loadFootprints()

    def onTreeFootprintsSelChanged( self, event ):
        if self.edit_state:
            return
        item = self.tree_footprints.GetSelection()
        if item.IsOk()==False:
            return
        footprintobj = self.tree_footprints_manager.ItemToObject(item)
        if isinstance(footprintobj, DataModelFootprint)==False:
            self.show_footprint(None)
            return
        self.panel_edit_footprint.SetFootprint(footprintobj.footprint)

        self.show_footprint(footprintobj.footprint)

    def onTreeFootprintsBeforeContextMenu( self, event ):
        item = self.tree_footprints.GetSelection()
        if item.IsOk()==False:
            return    
        obj = self.tree_footprints_manager.ItemToObject(item)

        self.menu_footprints_add.Enable(True)
        self.menu_footprints_delete.Enable(True)
        self.menu_footprints_edit.Enable(True)
        if isinstance(obj, DataModelFootprint):
            self.menu_footprints_add.Enable(False)
        else:
            self.menu_footprints_delete.Enable(False)
            self.menu_footprints_edit.Enable(False)


    def onEditFootprintApply( self, event ):
        footprint = event.data
        footprint_name = event.footprint_name
                
        if self.edit_state=='add':
            # get library path
            library_path = ''
            footprint_path = os.path.join(footprint.source_path, footprint_name)
            try:
                self.manager_pretty.CreateFile(footprint_path, footprint.content)
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), 'Error creating footprint', wx.OK | wx.ICON_ERROR)                                    
                return
            
        elif self.edit_state=='edit':
            # change library name if changed on disk
            library_path = os.path.dirname(footprint.source_path)
            footprint_path = os.path.normpath(os.path.join(library_path, footprint_name))
            
            if os.path.normpath(footprint.source_path)!=footprint_path:
                # file was renamed
                if self.tree_footprints.GetSelection().IsOk():
                    footprintobj = self.tree_footprints_manager.ItemToObject(self.tree_footprints.GetSelection())
                    try:
                        footprintobj.footprint = self.manager_pretty.MoveFile(footprint.source_path, os.path.join(library_path, footprint_name))
                    except Exception as e:
                        print_stack()
                        wx.MessageBox(format(e), 'Error renaming footprint', wx.OK | wx.ICON_ERROR)                                    
                        return
            try:
                if footprint.content:
                    self.manager_pretty.EditFile(footprint_path, footprint.content, create=True)
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), 'Error editing footprint', wx.OK | wx.ICON_ERROR)                                    
                return
            
        else:
            return
        
        self.manager_pretty.EditMetadata(footprint_path, footprint.metadata)
        
        self.edit_state = None
        self.show_footprint(footprint)

        self.load()

    def onEditFootprintCancel( self, event ):
        footprint = None
        item = self.tree_footprints.GetSelection()
        if item.IsOk():
            obj = self.tree_footprints_manager.ItemToObject(item)
            if isinstance(obj, DataModelFootprint):
                footprint = obj.footprint                
        self.edit_state = None
        self.show_footprint(footprint)
    
    def onToggleFootprintPathClicked( self, event ):
        self.show_footprint_path = self.toolbar_footprint.GetToolState(self.toggle_footprint_path.GetId())
        self.load()
        
    def onToggleShowBothChangesClicked( self, event ):
        self.show_both_changes = self.toolbar_footprint.GetToolState(self.toggle_show_both_changes.GetId())
        self.load()
    
    def onToggleShowConflictChangesClicked( self, event ):
        self.show_conflict_changes = self.toolbar_footprint.GetToolState(self.toggle_show_conflict_changes.GetId())
        self.load()
    
    def onToggleShowIncomingChangesClicked( self, event ):
        self.show_incoming_changes = self.toolbar_footprint.GetToolState(self.toggle_show_incoming_changes.GetId())
        self.load()
    
    def onToggleShowOutgoingChangesClicked( self, event ):
        self.show_outgoing_changes = self.toolbar_footprint.GetToolState(self.toggle_show_outgoing_changes.GetId())
        self.load()

    def onButtonRefreshFootprintsClick( self, event ):
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
                self.manager_pretty.CreateFolder(os.path.join(path, name))
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
                self.manager_pretty.CreateFolder(os.path.join(path, name+".pretty"))
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
                    self.manager_pretty.MoveFolder(path, newpath)
                except Exception as e:
                    print_stack()
                    wx.MessageBox(format(e), 'Error renaming folder', wx.OK | wx.ICON_ERROR)
            dlg.Destroy()
        elif isinstance(obj, DataModelLibrary):
            dlg = wx.TextEntryDialog(self, 'Enter new library name', 'Rename library')
            if dlg.ShowModal() == wx.ID_OK:
                name = dlg.GetValue()
                try:
                    newpath = os.path.join(os.path.dirname(path), name+".pretty")
                    self.manager_pretty.MoveFolder(path, newpath)
                except Exception as e:
                    print_stack()
                    wx.MessageBox(format(e), 'Error renaming library', wx.OK | wx.ICON_ERROR)
            dlg.Destroy()
        
        print "****", self.manager_pretty.local_files
        self.load()
        print "++++", self.manager_pretty.local_files

    def onMenuLibrariesRemove( self, event ):
        item = self.tree_libraries.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_libraries_manager.ItemToObject(item)
        path = obj.path
        try:
            self.manager_pretty.DeleteFolder(path)
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Error removing %s:'%path, wx.OK | wx.ICON_ERROR)
        self.load()
        

    def onMenuLibrariesAddFootprint( self, event ):
        item = self.tree_libraries.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_libraries_manager.ItemToObject(item)
        if isinstance(obj, DataModelLibrary)==False:
            return

        self.edit_state = 'add'
        self.new_footprint(obj.path)


    def onMenuFootprintsUpdate( self, event ):
        files = []
        for item in self.tree_footprints.GetSelections():
            obj = self.tree_footprints_manager.ItemToObject(item)
            if isinstance(obj, DataModelFootprint):
                files.append(obj.footprint)
            elif isinstance(obj, DataModelFootprintPath):
                for child in obj.childs:
                    if isinstance(child, DataModelFootprint):
                        files.append(child.footprint)
        
        try:
            self.manager_pretty.Update(files) 
            self.load()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Upload failed', wx.OK | wx.ICON_ERROR)
    
    def onMenuFootprintsForceUpdate( self, event ):
        files = []
        for item in self.tree_footprints.GetSelections():
            obj = self.tree_footprints_manager.ItemToObject(item)
            if isinstance(obj, DataModelFootprint):
                files.append(obj.footprint)
            elif isinstance(obj, DataModelFootprintPath):
                if obj.childs:
                    for child in obj.childs:
                        if isinstance(child, DataModelFootprint):
                            files.append(child.footprint)
        
        try:
            if len(files)>0:
                self.manager_pretty.Update(files, force=True) 
            self.load()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Upload failed', wx.OK | wx.ICON_ERROR)
    
    def onMenuFootprintsCommit( self, event ):
        files = []
        for item in self.tree_footprints.GetSelections():
            obj = self.tree_footprints_manager.ItemToObject(item)
            if isinstance(obj, DataModelFootprint):
                files.append(obj.footprint)
            elif isinstance(obj, DataModelFootprintPath):
                for child in obj.childs:
                    if isinstance(child, DataModelFootprint):
                        files.append(child.footprint)
        
        try:
            self.manager_pretty.Commit(files) 
            self.load()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Commit failed', wx.OK | wx.ICON_ERROR)
            
    
    def onMenuFootprintsForceCommit( self, event ):
        files = []
        for item in self.tree_footprints.GetSelections():
            obj = self.tree_footprints_manager.ItemToObject(item)
            if isinstance(obj, DataModelFootprint):
                files.append(obj.footprint)
            elif isinstance(obj, DataModelFootprintPath):
                for child in obj.childs:
                    if isinstance(child, DataModelFootprint):
                        files.append(child.footprint)
        
        try:
            self.manager_pretty.Commit(files, force=True) 
            self.load()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Commit failed', wx.OK | wx.ICON_ERROR)

    def onMenuFootprintsAdd( self, event ):
        item = self.tree_footprints.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_footprints_manager.ItemToObject(item)
        if isinstance(obj, DataModelFootprintPath)==False:
            return

        self.edit_state = 'add'
        self.new_footprint(obj.path)
    
    def onMenuFootprintsEdit( self, event ):
        item = self.tree_footprints.GetSelection()
        if item.IsOk()==False:
            return
        footprintobj = self.tree_footprints_manager.ItemToObject(item)
        if isinstance(footprintobj, DataModelFootprint)==False:
            return
        state = footprintobj.footprint.state
        if state.rfind('income')!=-1 or state.rfind('conflict')!=-1:
            wx.MessageBox("Item should be updated prior to beeing edited", 'Can not edit', wx.OK | wx.ICON_ERROR)
            return
        
        self.edit_state = 'edit'
    
        self.edit_footprint(footprintobj.footprint)
    
    def onMenuFootprintsDelete( self, event ):
        files = []
        for item in self.tree_footprints.GetSelections():
            obj = self.tree_footprints_manager.ItemToObject(item)
            if isinstance(obj, DataModelFootprint):
                files.append(obj.footprint)
            elif isinstance(obj, DataModelFootprintPath):
                pass
        
        try:
            for file in files:
                self.manager_pretty.DeleteFile(file) 
            self.load()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Delete failed', wx.OK | wx.ICON_ERROR)

    def onSearchFootprintsButton( self, event ):
        return self.onSearchFootprintsTextEnter(event)
    
    def onSearchFootprintsTextEnter( self, event ):
        # set search filter
        self.footprints_filter.remove('search')
        if self.search_footprints.Value!='':
            self.footprints_filter.add('search', self.search_footprints.Value)
        # apply new filter and reload
        self.loadFootprints()
