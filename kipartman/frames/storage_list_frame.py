from dialogs.panel_storage_list import PanelStorageList
import frames.edit_storage_frame
from frames.select_storage_frame import SelectStorageFrame, EVT_SELECT_STORAGE_OK_EVENT
from frames.dropdown_dialog import DropdownDialog
from frames.models.tree_manager_storages import StorageCategory, Storage, TreeManagerStorages
import api.data.storage
import helper.filter
from helper.log import log
from helper.profiler import Trace
import wx
from helper.exception import print_stack


(EnterEditModeEvent, EVT_ENTER_EDIT_MODE) = wx.lib.newevent.NewEvent()
(ExitEditModeEvent, EVT_EXIT_EDIT_MODE) = wx.lib.newevent.NewEvent()

class StorageListFrame(PanelStorageList): 
    def __init__(self, *args, **kwargs): 
        super(StorageListFrame, self).__init__(*args, **kwargs)

        # storages filters
        self._filters = helper.filter.FilterSet(self, self.toolbar_filters)
        self.Filters.Bind( helper.filter.EVT_FILTER_CHANGED, self.onFilterChanged )
        
        # create storage list
        self.tree_storages_manager = TreeManagerStorages(self.tree_storages, context_menu=self.menu_storage, filters=self.Filters)
        self.tree_storages_manager.OnSelectionChanged = self.onTreeStoragesSelectionChanged
        self.tree_storages_manager.OnItemBeforeContextMenu = self.onTreeStoragesBeforeContextMenu

        # create edit storage panel
        self.panel_edit_storage = frames.edit_storage_frame.EditStorageFrame(self.splitter_horz)

        # organize panels
        self.splitter_horz.Unsplit()
        self.splitter_horz.SplitHorizontally( self.panel_storage_locations, self.panel_edit_storage)
        self.panel_down.Hide()

        # initial state
        self.toolbar_storage.ToggleTool(self.toggle_storage_path.GetId(), True)
        self.Flat = False
        self.EditMode = False
        
    @property
    def Filters(self):
        return self._filters

    @property
    def Flat(self):
        return self.tree_storages_manager.flat
    
    @Flat.setter
    def Flat(self, value):
        self.tree_storages_manager.flat = value
        self.tree_storages_manager.Clear()
        self.tree_storages_manager.Load()
        self._expand_categories()
    
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
        self.tree_storages_manager.Load()

    def _expand_categories(self):
        if self.Flat==False:
            for category in self.tree_storages_manager.FindCategories():
                self.tree_storages_manager.Expand(category)
    
    def _enable(self, value):
        self.panel_up.Enabled = value


    def SetStorage(self, storage):
        self.panel_edit_storage.SetStorage(storage)
        self._enable(True)
        
    def EditStorage(self, storage):
        self.EditMode = True
        self.panel_edit_storage.EditStorage(storage)
        self._enable(False)
        

    def onToggleCategoryPathClicked( self, event ):
        self.Flat = not self.toolbar_storage.GetToolState(self.toggle_storage_path.GetId())
        event.Skip()

    def onButtonRefreshStoragesClick( self, event ):
        self.tree_storages_manager.Load()
        event.Skip()
        
    def onFilterChanged( self, event ):
        self.tree_storages_manager.Load()
        self._expand_categories()
        event.Skip()

    def onTreeStoragesSelectionChanged( self, event ):
        item = self.tree_storages.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_storages_manager.ItemToObject(item)
        if isinstance(obj, Storage):
            self.SetStorage(obj.storage)
        event.Skip()

    def onTreeStoragesBeforeContextMenu( self, event ):
        item = self.tree_storages.GetSelection()
        obj = None
        if item.IsOk():
            obj = self.tree_storages_manager.ItemToObject(item)

        self.menu_storage_add_storage.Enable(True)
        self.menu_storage_edit_storage.Enable(True)
        self.menu_storage_remove_storage.Enable(True)
        self.menu_storage_duplicate_storage.Enable(True)
        self.menu_storage_append_equivalent.Enable(True)
        if isinstance(obj, Storage)==False:
            self.menu_storage_edit_storage.Enable(False)
            self.menu_storage_remove_storage.Enable(False)
            self.menu_storage_duplicate_storage.Enable(False)
            self.menu_storage_append_equivalent.Enable(False)
        event.Skip()

    def onMenuStorageAddStorage( self, event ):
        item = self.tree_storages.GetSelection()
        category = None
        if item.IsOk():
            obj = self.tree_storages_manager.ItemToObject(item)
            if isinstance(obj, StorageCategory):
                category = obj.category
            elif isinstance(obj, Storage):
                category = obj.storage.category
        else:
            # add category from filter
            category = None
            if len(self.Filters.get_filters_group('category'))==1:
                category = self.Filters.get_filters_group('category')[0].category

        self.AddStorage(category)
        event.Skip()

    def onMenuStorageEditStorage( self, event ):
        item = self.tree_storages.GetSelection()
        if not item.IsOk():
            return
        obj = self.tree_storages_manager.ItemToObject(item)
        if isinstance(obj, Storage)==False:
            return
        self.EditStorage(obj.storage)
        event.Skip()

    def onMenuStorageRemoveStorage( self, event ):
        item = self.tree_storages.GetSelection()
        if not item.IsOk():
            return
        obj = self.tree_storages_manager.ItemToObject(item)
        if isinstance(obj, Storage)==False:
            return
        storage = obj.storage
        if isinstance(obj.parent, Storage):
            parent = obj.parent.storage
            res = wx.MessageDialog(self, "Remove storage '"+storage.name+"' from '"+parent.name+"'", "Remove?", wx.OK|wx.CANCEL).ShowModal()
            if res==wx.ID_OK:
                # remove selected storage from substorages
                parent = rest.api.find_storage(parent.id, with_childs=True)
                for child in parent.childs:
                    if child.id==storage.id:
                        parent.childs.remove(child)
 
                #parent.childs.remove(storage)
                rest.api.update_storage(parent.id, parent)
                self.tree_storages_manager.DeleteChildStorage(parent, storage)
            else:
                return 
        else:
            res = wx.MessageDialog(self, "Remove storage '"+storage.name+"'", "Remove?", wx.OK|wx.CANCEL).ShowModal()
            if res==wx.ID_OK:
                try:
                    # remove storage
                    api.data.storage.delete(storage)
                except Exception as e:
                    print_stack()
                    wx.MessageBox(format(e), 'Error updating stock', wx.OK | wx.ICON_ERROR)
                    return
            else:
                return
        self.SetStorage(None)
        
        self.tree_storages_manager.Load()
        event.Skip()

    def onMenuStorageDuplicateStorage( self, event ):
        item = self.tree_storages.GetSelection()
        if not item.IsOk():
            return
        obj = self.tree_storages_manager.ItemToObject(item)
        if isinstance(obj, Storage)==False:
            return

        storage = api.data.storage.duplicate(obj.storage)
        self.EditStorage(storage)
        event.Skip()
        
    def onEditStorageApply( self, event ):
        self.tree_storages_manager.Load()

        storage = event.storage
        storageobj = self.tree_storages_manager.FindStorage(storage.id)
        self.tree_storages_manager.Select(storageobj)
        
        self.SetStorage(storage)
        self.EditMode = False
        event.Skip()
      
    def onEditStorageCancel( self, event ):
        self.tree_storages_manager.Load()
        
        # reload the storage after changing it
        item = self.tree_storages.GetSelection()
        obj = self.tree_storages_manager.ItemToObject(item)
        if isinstance(obj, Storage):
            self.SetStorage(obj.storage)
        else:
            self.SetStorage(None)

        self.EditMode = False        
        event.Skip()

